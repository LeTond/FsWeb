from django.urls import path
from .views import IndexView, CreateProjectView, ViewerView, ProjectsView, \
    ProjectEditView, ProjectDeleteView, SubjectsInProjectView, SubjectDeleteView, SubjectEditView, \
    SubjectsView, StatisticView, CompareSubjectsView, InfoView, LieViewerView, InstructionsView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('new_project/', CreateProjectView.as_view(), name='new-project'),
    path('open_viewer/', ViewerView.as_view(), name='viewer'),
    path('open_info/', InfoView.as_view(), name='info'),
    path('open_lie_viewer/', LieViewerView.as_view(), name='lie-viewer'),
    path('open_instructions/', InstructionsView.as_view(), name='instructs'),

    # View
    path('project_list/', ProjectsView.as_view(), name='projects'),
    path('subject_list/', SubjectsView.as_view(), name='subjects'),
    path('subj_stats/<int:subject_id>/', StatisticView.as_view(), name='subj-stats'),

    # Edit
    path('project_edit/<int:project_id>/', ProjectEditView.as_view(), name='edit-project'),
    path('subject_edit/<int:subject_id>/', SubjectEditView.as_view(), name='edit-subject'),

    # Filter
    # path('filter_stats/<int:subject_id>/', FilterStatisticView.as_view(), name='filter-stats'),
    path('subjects_in_project/<int:project_id>/', SubjectsInProjectView.as_view(),
         name='subjects_in_project'),

    # Delete
    path('project_delete/<int:project_id>/', ProjectDeleteView.as_view(), name='delete-project'),
    path('subject_delete/<int:subject_id>/', SubjectDeleteView.as_view(), name='delete-subject'),

    # Compare
    path('subject_compare/', CompareSubjectsView.as_view(), name='compare_with'),
]