from django.contrib import admin
from .models import FormatDocument
from .models import StatusOfDocument
from .models import PrefixDecimalNumber
from .models import CipherProduct
from .models import TypeOfFile
from .models import TypeDesignDocument
from .models import DesignDocument
from .models import FileDesignDocument
from .models import CorrectionDesignDocument


admin.site.register(FormatDocument)
admin.site.register(StatusOfDocument)
admin.site.register(PrefixDecimalNumber)
admin.site.register(CipherProduct)
admin.site.register(TypeOfFile)
admin.site.register(TypeDesignDocument)
admin.site.register(DesignDocument)
admin.site.register(FileDesignDocument)
admin.site.register(CorrectionDesignDocument)


