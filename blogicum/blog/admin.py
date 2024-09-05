from django.contrib import admin

from .models import Category, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {'fields': ('title', 'description', 'slug')}),
        ('Публикация', {'fields': ('is_published',)}),
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at')
    search_fields = ('name',)
    fieldsets = (
        (None, {'fields': ('name',)}),
        ('Публикация', {'fields': ('is_published',)}),
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pub_date',
                    'category', 'is_published', 'created_at')
    list_filter = ('is_published', 'created_at', 'category')
    search_fields = ('title', 'text')
    date_hierarchy = 'pub_date'
    fieldsets = (
        (None, {'fields': ('title', 'text', 'pub_date',
         'author', 'category', 'location')}),
        ('Публикация', {'fields': ('is_published',)}),
    )
