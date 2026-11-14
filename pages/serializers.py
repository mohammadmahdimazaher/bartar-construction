from rest_framework import serializers

from .models import SitePage


class SitePageSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = SitePage
        fields = [
            "id",
            "key",
            "title",
            "subtitle",
            "content",
            "image",
            "images",
            "updated_at",
        ]

    def get_images(self, obj):
        request = self.context.get("request")
        files = [obj.image] if obj.image else []
        files += [item.image for item in obj.gallery.all() if item.image]

        urls = []
        for file in files:
            url = file.url
            urls.append(request.build_absolute_uri(url) if request else url)
        return urls
