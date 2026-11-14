from django.db import models

from projects.validators import validate_image_size


class SitePage(models.Model):
    SECTIONS = [
        ("about", "درباره ما"),
        ("community", "جامعه و مسئولیت"),
        ("services", "خدمات"),
        ("approach", "رویکرد ما"),
    ]

    key = models.CharField(
        max_length=30,
        choices=SECTIONS,
        unique=True,
        verbose_name="بخش",
    )
    title = models.CharField(max_length=200, verbose_name="عنوان")
    subtitle = models.CharField(
        max_length=300, blank=True, verbose_name="زیرعنوان")
    content = models.TextField(blank=True, verbose_name="متن")
    image = models.ImageField(
        upload_to="pages/sections/",
        blank=True,
        null=True,
        validators=[validate_image_size],
        verbose_name="عکس اول",
    )
    is_published = models.BooleanField(default=True, verbose_name="منتشر شود")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "بخش سایت"
        verbose_name_plural = "بخش‌های سایت"

    def __str__(self):
        return self.get_key_display()


class SitePageImage(models.Model):
    page = models.ForeignKey(
        SitePage,
        on_delete=models.CASCADE,
        related_name="gallery",
    )
    image = models.ImageField(
        upload_to="pages/sections/gallery/",
        validators=[validate_image_size],
        verbose_name="عکس",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب")

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "عکس گالری"
        verbose_name_plural = "عکس‌های گالری"

    def __str__(self):
        return f"{self.page} - {self.id}"
