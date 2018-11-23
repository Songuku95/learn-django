import uuid

from django.core.files.storage import FileSystemStorage
from django.views.decorators.http import require_POST

from commonlib.core import SuccessResponse, require_auth
from errors import InvalidRequestParams, FileTooLarge

MAX_IMAGE_FILE_SIZE = 4 * 1024 * 1024


@require_POST
@require_auth('member')
def upload_image(request, user):
	if not request.FILES.get('file'):
		raise InvalidRequestParams()
	file = request.FILES.get('file')
	if file.size > MAX_IMAGE_FILE_SIZE:
		raise FileTooLarge
	extention = file.name.split('.')[-1]
	fs = FileSystemStorage()
	filename = fs.save(str(uuid.uuid4()) + '.' + extention, file)
	uploaded_file_path = fs.url(filename)
	return SuccessResponse({
		'image_path': uploaded_file_path
	})
