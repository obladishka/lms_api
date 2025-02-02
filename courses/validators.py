import re

from rest_framework import serializers

from config.settings import ALLOWED_LESSON_DOMAINS


class URLValidator:
    """Class for validating course URLs."""

    def __init__(self):
        self.domain_pattern = r"(https?://)?(www\d?\.)?(?P<domain>[\w\.-]+\.\w+)(/\S*)?"

    def extract_domain(self, url):
        """Method for domain extraction."""
        match = re.match(self.domain_pattern, url)
        domain = match.group("domain")
        return domain

    def __call__(self, url):
        domain = self.extract_domain(url)
        if domain and domain not in ALLOWED_LESSON_DOMAINS:
            raise serializers.ValidationError("Link for third-party resources are not allowed.")
