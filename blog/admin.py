from django.contrib import admin

from .models import Author,Tag,Post,Comment,Token,Ormq
# Register your models here.

class Postadmin(admin.ModelAdmin):
    list_filters =('title','date')
    list_display =('title','date','author',)
    prepopulated_fields ={'slug':('title',)}

class Commentadmin(admin.ModelAdmin):
    list_display =['user_name','post']


admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Post,Postadmin)
admin.site.register(Comment,Commentadmin)
admin.site.register(Token)
admin.site.register(Ormq)