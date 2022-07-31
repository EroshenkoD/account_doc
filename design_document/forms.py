from django.forms import ModelForm, TextInput, Select
from .models import CipherProduct
from .models import PrefixDecimalNumber
from .models import TypeDesignDocument


class CipherPrfrom django.forms import ModelForm, TextInput, Select
from .models import CipherProduct
from .models import PrefixDecimalNumber
from .models import TypeDesignDocument


class CipherProductForms(ModelForm):
    class Meta:
        model = CipherProduct
        fields = ['cipher_of_product', 'description_cipher_of_product']

        widgets = {
            "cipher_of_product": Select(attrs={'class': 'form-select'})
        }
