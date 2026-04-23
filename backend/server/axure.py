from pathlib import Path

from django.conf import settings
from django.http import Http404
from django.views.static import serve


def axure_serve(request, path):
    if not settings.DEBUG:
        raise Http404()
    root_dir = Path(__file__).resolve().parents[2]
    full_path = (root_dir / path).resolve()
    if root_dir not in full_path.parents and full_path != root_dir:
        raise Http404()
    return serve(request, path, document_root=str(root_dir))

