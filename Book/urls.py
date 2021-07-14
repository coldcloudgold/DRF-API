from rest_framework.routers import SimpleRouter

from .views import BookViewSet, UserBookRelationView


router = SimpleRouter()

router.register(r"book", BookViewSet)
router.register(r"book_relation", UserBookRelationView)

urlpatterns = router.urls
