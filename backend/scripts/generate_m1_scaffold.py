from pathlib import Path


def build_files():
    """Build a mapping from relative file path to file content."""
    files = {}
    files["requirements.txt"] = """Django==4.2.16
djangorestframework==3.15.2
djangorestframework-simplejwt==5.3.1
django-cors-headers==4.4.0
mysqlclient==2.2.4
"""
    files["apps/__init__.py"] = ""
    apps = [
        "common",
        "authn",
        "master_data",
        "calc_config",
        "data_entry",
        "calculation",
        "reports",
        "analytics",
        "assets",
    ]
    for app in apps:
        class_name = "".join(part.capitalize() for part in app.split("_")) + "Config"
        files[f"apps/{app}/apps.py"] = (
            "from django.apps import AppConfig\n\n\n"
            f"class {class_name}(AppConfig):\n"
            '    default_auto_field = "django.db.models.BigAutoField"\n'
            f'    name = "apps.{app}"\n'
        )

    files["apps/common/response.py"] = """from rest_framework.response import Response


def ok(data=None, message="ok"):
    \"\"\"Return a success response with unified payload.\"\"\"
    return Response({"code": 0, "message": message, "data": data or {}})


def fail(message="error", code=50000, data=None, status=400):
    \"\"\"Return an error response with unified payload.\"\"\"
    return Response({"code": code, "message": message, "data": data or {}}, status=status)
"""
    files["apps/common/pagination.py"] = """from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    \"\"\"Provide a consistent page/page_size pagination contract.\"\"\"
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 200
"""
    files["apps/authn/models.py"] = """from django.conf import settings
from django.db import models


class Role(models.Model):
    \"\"\"Store role definitions for RBAC.\"\"\"
    code = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        \"\"\"Return role display name.\"\"\"
        return self.name


class Menu(models.Model):
    \"\"\"Store navigable menu items and route definitions.\"\"\"
    name = models.CharField(max_length=128)
    path = models.CharField(max_length=256)
    component = models.CharField(max_length=256, blank=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE, related_name="children")
    sort = models.IntegerField(default=0)

    class Meta:
        ordering = ["sort", "id"]


class UserRole(models.Model):
    \"\"\"Map user to role.\"\"\"
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "role")


class RoleMenu(models.Model):
    \"\"\"Map role to menu.\"\"\"
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("role", "menu")
"""
    files["apps/authn/serializers.py"] = """from django.contrib.auth.models import User
from rest_framework import serializers

from apps.authn.models import Menu


class LoginSerializer(serializers.Serializer):
    \"\"\"Validate login payload.\"\"\"
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    \"\"\"Serialize minimal user info for current session.\"\"\"

    class Meta:
        model = User
        fields = ["id", "username", "is_staff", "is_superuser"]


class MenuSerializer(serializers.ModelSerializer):
    \"\"\"Serialize menu tree nodes.\"\"\"
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ["id", "name", "path", "component", "sort", "children"]

    def get_children(self, obj):
        \"\"\"Return nested children menus in order.\"\"\"
        return MenuSerializer(obj.children.order_by("sort", "id"), many=True).data
"""
    files["apps/authn/views.py"] = """from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authn.models import Menu
from apps.authn.serializers import LoginSerializer, UserSerializer, MenuSerializer
from apps.common.response import ok, fail


def get_tokens_for_user(user):
    \"\"\"Build access and refresh JWT token pair for a user.\"\"\"
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    \"\"\"Authenticate user and return token plus profile payload.\"\"\"
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(
        username=serializer.validated_data["username"],
        password=serializer.validated_data["password"],
    )
    if not user:
        return fail(message="用户名或密码错误", code=40001, status=400)
    tokens = get_tokens_for_user(user)
    return ok({"tokens": tokens, "user": UserSerializer(user).data})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):
    \"\"\"Return current authenticated user profile.\"\"\"
    return ok(UserSerializer(request.user).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def menus_view(request):
    \"\"\"Return simple static menu tree for M1 pages.\"\"\"
    roots = Menu.objects.filter(parent__isnull=True).order_by("sort", "id")
    if not roots.exists():
        return ok(
            [
                {"name": "仪表盘", "path": "/dashboard", "component": "DashboardView"},
                {"name": "燃料品种", "path": "/master/fuels", "component": "FuelTypeView"},
                {"name": "生产用料", "path": "/master/materials", "component": "MaterialView"},
                {"name": "核算配置", "path": "/calc/templates", "component": "CalcTemplateView"},
                {"name": "数据填报", "path": "/calc/entries", "component": "DataEntryView"},
                {"name": "报告管理", "path": "/calc/reports", "component": "ReportView"},
            ]
        )
    return ok(MenuSerializer(roots, many=True).data)


@api_view(["POST"])
@permission_classes([AllowAny])
def bootstrap_admin(request):
    \"\"\"Create default admin account for local bootstrap if absent.\"\"\"
    username = request.data.get("username", "admin")
    password = request.data.get("password", "Admin@123456")
    if User.objects.filter(username=username).exists():
        return ok({"username": username}, message="用户已存在")
    user = User.objects.create_superuser(username=username, password=password)
    return ok(UserSerializer(user).data, message="管理员创建成功")
"""
    files["apps/authn/urls.py"] = """from django.urls import path

from apps.authn.views import login_view, me_view, menus_view, bootstrap_admin

urlpatterns = [
    path("login", login_view),
    path("me", me_view),
    path("menus", menus_view),
    path("bootstrap-admin", bootstrap_admin),
]
"""
    files["apps/master_data/models.py"] = """from django.db import models


class FuelType(models.Model):
    \"\"\"Store fuel type master data and factor settings.\"\"\"
    name = models.CharField(max_length=128, unique=True)
    category = models.CharField(max_length=64, default="化石燃料")
    form = models.CharField(max_length=64, default="固态")
    alias = models.CharField(max_length=128, blank=True)
    carbon_content = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    oxidation_rate = models.DecimalField(max_digits=8, decimal_places=4, default=0)
    emission_factor = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]


class Material(models.Model):
    \"\"\"Store production material and process links for accounting.\"\"\"
    name = models.CharField(max_length=128, unique=True)
    process_link = models.CharField(max_length=255, blank=True)
    emission_factor = models.DecimalField(max_digits=12, decimal_places=4, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]
"""
    files["apps/master_data/serializers.py"] = """from rest_framework import serializers

from apps.master_data.models import FuelType, Material


class FuelTypeSerializer(serializers.ModelSerializer):
    \"\"\"Serialize fuel type records.\"\"\"

    class Meta:
        model = FuelType
        fields = "__all__"


class MaterialSerializer(serializers.ModelSerializer):
    \"\"\"Serialize material records.\"\"\"

    class Meta:
        model = Material
        fields = "__all__"
"""
    files["apps/master_data/views.py"] = """from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.common.pagination import StandardResultsSetPagination
from apps.master_data.models import FuelType, Material
from apps.master_data.serializers import FuelTypeSerializer, MaterialSerializer


class FuelTypeViewSet(viewsets.ModelViewSet):
    \"\"\"Provide CRUD endpoints for fuel types.\"\"\"
    queryset = FuelType.objects.all()
    serializer_class = FuelTypeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class MaterialViewSet(viewsets.ModelViewSet):
    \"\"\"Provide CRUD endpoints for production materials.\"\"\"
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
"""
    files["apps/master_data/urls.py"] = """from rest_framework.routers import DefaultRouter

from apps.master_data.views import FuelTypeViewSet, MaterialViewSet

router = DefaultRouter()
router.register("fuels", FuelTypeViewSet, basename="fuels")
router.register("materials", MaterialViewSet, basename="materials")

urlpatterns = router.urls
"""
    files["apps/calc_config/models.py"] = """from django.db import models


class CalcTemplate(models.Model):
    \"\"\"Store accounting template metadata by industry.\"\"\"
    name = models.CharField(max_length=128)
    industry = models.CharField(max_length=128)
    version = models.CharField(max_length=32, default="v1")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]


class CalcBoundaryItem(models.Model):
    \"\"\"Store configurable boundary items under a template.\"\"\"
    template = models.ForeignKey(CalcTemplate, on_delete=models.CASCADE, related_name="boundary_items")
    name = models.CharField(max_length=128)
    item_type = models.CharField(max_length=64, default="过程排放")
    formula = models.TextField(blank=True)
    factor_ref = models.CharField(max_length=128, blank=True)
    sort = models.IntegerField(default=0)
    is_enabled = models.BooleanField(default=True)

    class Meta:
        ordering = ["sort", "id"]


class CalcFactor(models.Model):
    \"\"\"Store factor values with version and effective date.\"\"\"
    name = models.CharField(max_length=128)
    factor_type = models.CharField(max_length=64, default="排放因子")
    unit = models.CharField(max_length=32, blank=True)
    value = models.DecimalField(max_digits=16, decimal_places=6, default=0)
    version = models.CharField(max_length=32, default="v1")
    effective_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]
"""
    files["apps/calc_config/serializers.py"] = """from rest_framework import serializers

from apps.calc_config.models import CalcTemplate, CalcBoundaryItem, CalcFactor


class CalcBoundaryItemSerializer(serializers.ModelSerializer):
    \"\"\"Serialize template boundary item records.\"\"\"

    class Meta:
        model = CalcBoundaryItem
        fields = "__all__"


class CalcTemplateSerializer(serializers.ModelSerializer):
    \"\"\"Serialize templates and nested boundary items.\"\"\"
    boundary_items = CalcBoundaryItemSerializer(many=True, read_only=True)

    class Meta:
        model = CalcTemplate
        fields = "__all__"


class CalcFactorSerializer(serializers.ModelSerializer):
    \"\"\"Serialize factor records.\"\"\"

    class Meta:
        model = CalcFactor
        fields = "__all__"
"""
    files["apps/calc_config/views.py"] = """from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.calc_config.models import CalcTemplate, CalcBoundaryItem, CalcFactor
from apps.calc_config.serializers import CalcTemplateSerializer, CalcBoundaryItemSerializer, CalcFactorSerializer
from apps.common.pagination import StandardResultsSetPagination


class CalcTemplateViewSet(viewsets.ModelViewSet):
    \"\"\"Provide CRUD endpoints for accounting templates.\"\"\"
    queryset = CalcTemplate.objects.all()
    serializer_class = CalcTemplateSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class CalcBoundaryItemViewSet(viewsets.ModelViewSet):
    \"\"\"Provide CRUD endpoints for template boundary items.\"\"\"
    queryset = CalcBoundaryItem.objects.all()
    serializer_class = CalcBoundaryItemSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination


class CalcFactorViewSet(viewsets.ModelViewSet):
    \"\"\"Provide CRUD endpoints for factor management.\"\"\"
    queryset = CalcFactor.objects.all()
    serializer_class = CalcFactorSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
"""
    files["apps/calc_config/urls.py"] = """from rest_framework.routers import DefaultRouter

from apps.calc_config.views import CalcTemplateViewSet, CalcBoundaryItemViewSet, CalcFactorViewSet

router = DefaultRouter()
router.register("templates", CalcTemplateViewSet, basename="calc-templates")
router.register("boundary-items", CalcBoundaryItemViewSet, basename="boundary-items")
router.register("factors", CalcFactorViewSet, basename="factors")

urlpatterns = router.urls
"""
    files["apps/data_entry/models.py"] = """from django.conf import settings
from django.db import models


class EntryMonthlyData(models.Model):
    \"\"\"Store monthly submission header records.\"\"\"
    STATUS_CHOICES = [
        ("draft", "草稿"),
        ("submitted", "已提交"),
    ]

    year = models.IntegerField()
    month = models.IntegerField()
    org_name = models.CharField(max_length=255)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="draft")
    remark = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-year", "-month", "-id"]


class EntryMonthlyItem(models.Model):
    \"\"\"Store monthly submission detail line items.\"\"\"
    entry = models.ForeignKey(EntryMonthlyData, on_delete=models.CASCADE, related_name="items")
    energy_type = models.CharField(max_length=64)
    sub_type = models.CharField(max_length=128, blank=True)
    value = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    cost = models.DecimalField(max_digits=16, decimal_places=4, default=0)
"""
    files["apps/data_entry/serializers.py"] = """from rest_framework import serializers

from apps.data_entry.models import EntryMonthlyData, EntryMonthlyItem


class EntryMonthlyItemSerializer(serializers.ModelSerializer):
    \"\"\"Serialize monthly data detail items.\"\"\"

    class Meta:
        model = EntryMonthlyItem
        fields = "__all__"


class EntryMonthlyDataSerializer(serializers.ModelSerializer):
    \"\"\"Serialize monthly data headers and nested items.\"\"\"
    items = EntryMonthlyItemSerializer(many=True)

    class Meta:
        model = EntryMonthlyData
        fields = "__all__"

    def create(self, validated_data):
        \"\"\"Create monthly header and all nested detail items.\"\"\"
        items = validated_data.pop("items", [])
        instance = EntryMonthlyData.objects.create(**validated_data)
        EntryMonthlyItem.objects.bulk_create([EntryMonthlyItem(entry=instance, **item) for item in items])
        return instance

    def update(self, instance, validated_data):
        \"\"\"Update monthly header and replace nested detail items.\"\"\"
        items = validated_data.pop("items", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        if items is not None:
            instance.items.all().delete()
            EntryMonthlyItem.objects.bulk_create([EntryMonthlyItem(entry=instance, **item) for item in items])
        return instance
"""
    files["apps/data_entry/views.py"] = """from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.common.pagination import StandardResultsSetPagination
from apps.data_entry.models import EntryMonthlyData
from apps.data_entry.serializers import EntryMonthlyDataSerializer


class EntryMonthlyDataViewSet(viewsets.ModelViewSet):
    \"\"\"Provide CRUD endpoints for monthly data submissions.\"\"\"
    queryset = EntryMonthlyData.objects.prefetch_related("items").all()
    serializer_class = EntryMonthlyDataSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        \"\"\"Persist creator for traceability when creating records.\"\"\"
        serializer.save(created_by=self.request.user)
"""
    files["apps/data_entry/urls.py"] = """from rest_framework.routers import DefaultRouter

from apps.data_entry.views import EntryMonthlyDataViewSet

router = DefaultRouter()
router.register("entries", EntryMonthlyDataViewSet, basename="entries")

urlpatterns = router.urls
"""
    files["apps/calculation/models.py"] = """from django.db import models

from apps.data_entry.models import EntryMonthlyData


class CalcTask(models.Model):
    \"\"\"Store execution status of accounting calculation jobs.\"\"\"
    STATUS_CHOICES = [
        ("pending", "待执行"),
        ("running", "执行中"),
        ("success", "成功"),
        ("failed", "失败"),
    ]

    entry = models.ForeignKey(EntryMonthlyData, on_delete=models.CASCADE)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default="pending")
    message = models.CharField(max_length=255, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]


class CalcResult(models.Model):
    \"\"\"Store calculation summary metrics.\"\"\"
    task = models.OneToOneField(CalcTask, on_delete=models.CASCADE, related_name="result")
    total_emission = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    total_energy = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    intensity = models.DecimalField(max_digits=16, decimal_places=6, default=0)
    yoy = models.DecimalField(max_digits=8, decimal_places=4, default=0)


class CalcResultDetail(models.Model):
    \"\"\"Store calculation detail rows for display and export.\"\"\"
    result = models.ForeignKey(CalcResult, on_delete=models.CASCADE, related_name="details")
    metric_name = models.CharField(max_length=128)
    metric_value = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    unit = models.CharField(max_length=32, blank=True)
"""
    files["apps/calculation/serializers.py"] = """from rest_framework import serializers

from apps.calculation.models import CalcTask, CalcResult, CalcResultDetail


class CalcResultDetailSerializer(serializers.ModelSerializer):
    \"\"\"Serialize detailed metrics for a result.\"\"\"

    class Meta:
        model = CalcResultDetail
        fields = "__all__"


class CalcResultSerializer(serializers.ModelSerializer):
    \"\"\"Serialize calculation summary with detail metrics.\"\"\"
    details = CalcResultDetailSerializer(many=True, read_only=True)

    class Meta:
        model = CalcResult
        fields = "__all__"


class CalcTaskSerializer(serializers.ModelSerializer):
    \"\"\"Serialize calculation tasks and optional result.\"\"\"
    result = CalcResultSerializer(read_only=True)

    class Meta:
        model = CalcTask
        fields = "__all__"
"""
    files["apps/calculation/views.py"] = """from decimal import Decimal

from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.calculation.models import CalcTask, CalcResult, CalcResultDetail
from apps.calculation.serializers import CalcTaskSerializer
from apps.common.pagination import StandardResultsSetPagination
from apps.data_entry.models import EntryMonthlyData


class CalcTaskViewSet(viewsets.ModelViewSet):
    \"\"\"Provide task management and execution endpoint for calculations.\"\"\"
    queryset = CalcTask.objects.select_related("result", "entry").all()
    serializer_class = CalcTaskSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    @action(detail=False, methods=["post"])
    def run(self, request):
        \"\"\"Execute a simplified calculation task from an entry ID.\"\"\"
        entry_id = request.data.get("entry_id")
        if not entry_id:
            return Response({"code": 40001, "message": "entry_id 不能为空", "data": {}}, status=status.HTTP_400_BAD_REQUEST)
        try:
            entry = EntryMonthlyData.objects.prefetch_related("items").get(id=entry_id)
        except EntryMonthlyData.DoesNotExist:
            return Response({"code": 40004, "message": "填报数据不存在", "data": {}}, status=status.HTTP_404_NOT_FOUND)
        task = CalcTask.objects.create(entry=entry, status="running", started_at=timezone.now())
        total_energy = sum([item.value for item in entry.items.all()])
        total_emission = Decimal(total_energy) * Decimal("2.35")
        intensity = Decimal("0") if total_energy == 0 else total_emission / Decimal(total_energy)
        result = CalcResult.objects.create(
            task=task,
            total_emission=total_emission,
            total_energy=total_energy,
            intensity=intensity,
            yoy=Decimal("0.12"),
        )
        CalcResultDetail.objects.bulk_create(
            [
                CalcResultDetail(result=result, metric_name="总能耗", metric_value=total_energy, unit="吨标煤"),
                CalcResultDetail(result=result, metric_name="总排放", metric_value=total_emission, unit="吨CO2"),
            ]
        )
        task.status = "success"
        task.message = "计算成功"
        task.ended_at = timezone.now()
        task.save(update_fields=["status", "message", "ended_at"])
        serializer = self.get_serializer(task)
        return Response({"code": 0, "message": "ok", "data": serializer.data})
"""
    files["apps/calculation/urls.py"] = """from rest_framework.routers import DefaultRouter

from apps.calculation.views import CalcTaskViewSet

router = DefaultRouter()
router.register("tasks", CalcTaskViewSet, basename="calc-tasks")

urlpatterns = router.urls
"""
    files["apps/reports/models.py"] = """from django.db import models


class ReportRecord(models.Model):
    \"\"\"Store generated report metadata and summarized values.\"\"\"
    REPORT_CHOICES = [
        ("emission", "排放报告"),
        ("energy", "能耗报告"),
        ("warning", "告警报告"),
    ]
    name = models.CharField(max_length=255)
    report_type = models.CharField(max_length=32, choices=REPORT_CHOICES, default="emission")
    year = models.IntegerField()
    month = models.IntegerField(default=1)
    total_emission = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    total_energy = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    value_added = models.DecimalField(max_digits=16, decimal_places=4, default=0)
    file_path = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=32, default="generated")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]


class ReportAttachment(models.Model):
    \"\"\"Store report attachment records for download.\"\"\"
    report = models.ForeignKey(ReportRecord, on_delete=models.CASCADE, related_name="attachments")
    file_name = models.CharField(max_length=255)
    file_url = models.CharField(max_length=255)
"""
    files["apps/reports/serializers.py"] = """from rest_framework import serializers

from apps.reports.models import ReportRecord, ReportAttachment


class ReportAttachmentSerializer(serializers.ModelSerializer):
    \"\"\"Serialize report attachments.\"\"\"

    class Meta:
        model = ReportAttachment
        fields = "__all__"


class ReportRecordSerializer(serializers.ModelSerializer):
    \"\"\"Serialize reports and attachment list.\"\"\"
    attachments = ReportAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = ReportRecord
        fields = "__all__"
"""
    files["apps/reports/views.py"] = """from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from apps.common.pagination import StandardResultsSetPagination
from apps.reports.models import ReportRecord
from apps.reports.serializers import ReportRecordSerializer


class ReportRecordViewSet(viewsets.ModelViewSet):
    \"\"\"Provide report management APIs including download endpoint.\"\"\"
    queryset = ReportRecord.objects.prefetch_related("attachments").all()
    serializer_class = ReportRecordSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        \"\"\"Return a text report file for quick local verification.\"\"\"
        report = self.get_object()
        content = (
            f"报告名称: {report.name}\\n类型: {report.get_report_type_display()}\\n"
            f"年份: {report.year}\\n月份: {report.month}"
        )
        response = HttpResponse(content, content_type="text/plain; charset=utf-8")
        response["Content-Disposition"] = f"attachment; filename=report_{report.id}.txt"
        return response
"""
    files["apps/reports/urls.py"] = """from rest_framework.routers import DefaultRouter

from apps.reports.views import ReportRecordViewSet

router = DefaultRouter()
router.register("records", ReportRecordViewSet, basename="report-records")

urlpatterns = router.urls
"""
    files["apps/analytics/models.py"] = "from django.db import models\\n\\n# M2 扩展模型预留。\\n"
    files["apps/assets/models.py"] = "from django.db import models\\n\\n# M3 扩展模型预留。\\n"
    files["apps/analytics/urls.py"] = "urlpatterns = []\\n"
    files["apps/assets/urls.py"] = "urlpatterns = []\\n"
    files["server/settings.py"] = """import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key")
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "apps.common",
    "apps.authn",
    "apps.master_data",
    "apps.calc_config",
    "apps.data_entry",
    "apps.calculation",
    "apps.reports",
    "apps.analytics",
    "apps.assets",
]
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "server.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = "server.wsgi.application"
if os.getenv("USE_SQLITE", "true").lower() == "true":
    DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": os.getenv("MYSQL_DB", "carbon_assets_v2"),
            "USER": os.getenv("MYSQL_USER", "root"),
            "PASSWORD": os.getenv("MYSQL_PASSWORD", "root"),
            "HOST": os.getenv("MYSQL_HOST", "127.0.0.1"),
            "PORT": os.getenv("MYSQL_PORT", "3306"),
            "OPTIONS": {"charset": "utf8mb4"},
        }
    }
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
LANGUAGE_CODE = "zh-hans"
TIME_ZONE = "Asia/Shanghai"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
CORS_ALLOW_ALL_ORIGINS = True
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(os.getenv("JWT_ACCESS_MINUTES", "120"))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.getenv("JWT_REFRESH_DAYS", "7"))),
}
"""
    files["server/urls.py"] = """from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("apps.authn.urls")),
    path("api/v1/auth/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/master-data/", include("apps.master_data.urls")),
    path("api/v1/calc-config/", include("apps.calc_config.urls")),
    path("api/v1/data-entry/", include("apps.data_entry.urls")),
    path("api/v1/calculation/", include("apps.calculation.urls")),
    path("api/v1/reports/", include("apps.reports.urls")),
]
"""
    return files


def write_files():
    """Write generated files to backend directory."""
    root = Path(__file__).resolve().parent.parent
    files = build_files()
    for rel_path, content in files.items():
        full_path = root / rel_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding="utf-8")
    print(f"Wrote {len(files)} files.")


if __name__ == "__main__":
    write_files()
