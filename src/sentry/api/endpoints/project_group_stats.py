from __future__ import absolute_import

import six

from rest_framework.response import Response

from sentry.app import tsdb
from sentry.api.base import StatsMixin
from sentry.api.bases.project import ProjectEndpoint
from sentry.models import Group


class ProjectGroupStatsEndpoint(ProjectEndpoint, StatsMixin):
    def get(self, request, project):
        group_ids = request.GET.getlist('id')
        if not group_ids:
            return Response(status=204)

        group_list = Group.objects.filter(project=project, id__in=group_ids)
        group_ids = [g.id for g in group_list]

        if not group_ids:
            return Response(status=204)

        data = tsdb.get_range(model=tsdb.models.group, keys=group_ids, **self._parse_args(request))

        return Response({six.text_type(k): v for k, v in data.items()})
