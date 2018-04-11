import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name="grupo-dasa",
    api_key="677559119568421",
    api_secret="InknfkzrSjpeWNuW61nqaOjyEeI"
)


def create_file(file):
    return cloudinary.uploader.upload(file)
