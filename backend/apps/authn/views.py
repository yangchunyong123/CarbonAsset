from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from apps.authn.models import Menu
from apps.authn.serializers import LoginSerializer, UserSerializer, MenuSerializer
from apps.common.response import ok, fail


def get_tokens_for_user(user):
    """Build access and refresh JWT token pair for a user."""
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """Authenticate user and return token plus profile payload."""
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
    """Return current authenticated user profile."""
    return ok(UserSerializer(request.user).data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def menus_view(request):
    """Return simple static menu tree for M1 pages."""
    roots = Menu.objects.filter(parent__isnull=True).order_by("sort", "id")
    if not roots.exists():
        return ok(
            [
                {"name": "仪表盘", "path": "/dashboard", "component": "DashboardView"},
                {"name": "能碳总览", "path": "/calc/overview", "component": "CalcOverviewView"},
                {"name": "用电分析", "path": "/analysis/power", "component": "PowerAnalysisView"},
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
    """Create default admin account for local bootstrap if absent."""
    username = request.data.get("username", "admin")
    password = request.data.get("password", "Admin@123456")
    if User.objects.filter(username=username).exists():
        return ok({"username": username}, message="用户已存在")
    user = User.objects.create_superuser(username=username, password=password)
    return ok(UserSerializer(user).data, message="管理员创建成功")
