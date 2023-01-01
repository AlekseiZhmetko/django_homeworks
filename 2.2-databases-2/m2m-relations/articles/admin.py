from django.contrib import admin

from django.core.exceptions import ValidationError
from .models import Article, Tag, Scope
from django.forms import BaseInlineFormSet

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        unique_tags = []
        for form in self.forms:
            unique_tags.append(form.cleaned_data.get('is_main'))
        if unique_tags.count(True) != 1:
            raise ValidationError('Пожалуйста, выберите один основной раздел!')
        return super().clean()  # вызываем базовый код переопределяемого метода

class ScopeInline(admin.TabularInline):

    model = Scope
    formset = ScopeInlineFormset



@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
    pass

# @admin.register(Scope)
# class ScopeAdmin(admin.ModelAdmin):
#     pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass