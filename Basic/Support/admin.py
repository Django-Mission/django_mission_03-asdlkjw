from django.contrib import admin

from support.models import Answer, Faq, Inquiry

# Register your models here.

# - 자주묻는질문(`Faq`)
# - 목록페이지 출력 필드 : 제목, 카테고리, 최종 수정 일시
# - 검색 필드 : 제목
# - 필터 필드 : 카테고리
class CommentInline(admin.TabularInline):
    model = Answer
    extra = 3
    min_num = 0
    max_num = 5
    verbose_name = '댓글'
    verbose_name_plural = '댓글'

@admin.register(Faq)
class SupportModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'updated_at')
    list_filter = ('category',)
    search_fields = ('title','category')
    search_help_text = '제목 검색이 가능합니다.'
    readonly_fields = ('created_at',)

#------------------------------------------------------------------------
# - 1:1문의(`Inquiry`)
#     - 목록페이지 출력 필드 : 질문 제목, 카테고리, 생성 일시, 생성자
#     - 검색 필드 : 제목, 이메일, 전화번호
#     - 필터 필드 : 카테고리
#     - 인라인모델 : 답변(`Answer`)
# - 답변(`Answer`)
#     - 1:1문의 모델에 인라인모델로 추가
@admin.register(Inquiry)
class SupportModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at','created_by')
    list_filter = ('category',)
    search_fields = ('title','email','phone')
    search_help_text = '제목, 이메일, 전화번호 검색이 가능합니다.'
    readonly_fields = ('created_at',)
    inlines = [CommentInline]

    actions = ['make_published']

    def make_published(modeladmin, request, queryset):
        for item in queryset:
            item.content = '운영 규정 위반으로 인한 게시글 삭제 처리.'
            item.save()