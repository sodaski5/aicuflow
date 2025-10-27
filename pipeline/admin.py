from django.contrib import admin
from .models import Node
from .tasks import run_node  # celery task

@admin.register(Node)
class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'node_type', 'status', 'created_at', 'updated_at')
    list_filter = ('node_type', 'status')
    ordering = ('-created_at',)

    actions = ['run_selected_nodes']

    def run_selected_nodes(self, request, queryset):
        for node in queryset:
            run_node.delay(node.id)  # asynchronous execution
        self.message_user(request, "Selected nodes have been scheduled to run.")
    run_selected_nodes.short_description = "Run selected nodes"
