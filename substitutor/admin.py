from django.contrib import admin

# Register your models here.


from .models import Comment

def make_validation(modeladmin, request, queryset):
    queryset.update(validation_status='t')
make_validation.short_description = "Valider la publication de commentaire"

def remove_validation(modeladmin, request, queryset):
    queryset.update(validation_status='f')
remove_validation.short_description = "Masquer le commentaire"


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_filter = ['validation_status']
    list_display = ('contenu_text', 'validation_status', 'date_insertion')
    actions = [make_validation, remove_validation]