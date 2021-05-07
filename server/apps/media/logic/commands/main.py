from apps.media.logic.commands.image import upload_image

COMMANDS = ((upload_image.UploadImageCommand, upload_image.CommandHandler),)
