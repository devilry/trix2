from trix.trix_core import models as coremodels


def bulk_update_assignment_tags(assignments_by_tag, existing_assignments):
    """
    Bulk update assignment tags.

    Parameters:
        assignments_by_tag: A dict where the keys are tag strings, and the
            values are lists of :class:`trix.trix_core.models.Assignment`
            objects.
        existing_assignments:
            A list of existing assignments. Any assignment in this list
            gets their current tags cleared before we add the tags
            in ``assignments_by_tag``.

    Example::

        assignment1 = coremodels.Assignment.objects.create(
            title='A1', text='text1')
        assignment2 = coremodels.Assignment.objects.create(
            title='A2', text='text2')
        bulk_update_assignment_tags(
            assignments_by_tag={
                'duck1000': [assignment1, assignment2],
                'oblig2': [assignment1]
            },
            existing_assignments=[assignment1, assignment2])

    The example will set the duck1000 tag on both assignment1 and assignment2,
    and the oblig2 tag on assignment1.
    """
    AssignmentTag = coremodels.Assignment.tags.through

    # Clear the tags on the existing assignments
    if existing_assignments:
        AssignmentTag.objects\
            .filter(assignment__in=existing_assignments)\
            .delete()

    # Bulk create any missing tags
    existing_tags = coremodels.Tag.objects.filter(tag__in=list(assignments_by_tag.keys()))
    new_tags = set(assignments_by_tag.keys())
    new_tags.difference_update(set([tagobject.tag for tagobject in existing_tags]))
    new_tagobjects = [coremodels.Tag(tag=tag) for tag in new_tags]
    coremodels.Tag.objects.bulk_create(new_tagobjects)

    # Bulk add tags to the assignments
    assignmenttags = []
    for tagobject in coremodels.Tag.objects.filter(tag__in=list(assignments_by_tag.keys())):
        assignments = assignments_by_tag[tagobject.tag]
        for assignment in assignments:
            assignmenttags.append(AssignmentTag(tag=tagobject, assignment=assignment))
    AssignmentTag.objects.bulk_create(assignmenttags)
