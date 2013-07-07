from tastypie.resources import ModelResource

class SpecifiedFields(ModelResource):

    def get_object_list(self, request):

        filters = super(SpecifiedFields, self).build_filters()

        self.specified_fields = []

        objects = super(SpecifiedFields, self).get_object_list(request)

        distinct = request.GET.get('distinct', False) == 'true'
        fields = request.GET.get("fields", False)

        if not fields:
            return objects

        try:
            self.specified_fields = fields.split(',')
        except:
            self.specified_fields.append(fields)

        # make `distinct` default for m2m filters
        has_m2m = False
        for field in filters:
            try:
                related = objects.model._meta.get_field_by_name(field)[0]
            except:
                related = False
            if related and related.get_internal_type() == 'ManyToManyField':
                has_m2m = True

        only_fields = []
        select_related = []

        for specified_field in self.specified_fields:

            try:
                fields = specified_field.split('__')
            except:
                continue

            # Only adds fields that exist for this model
            # excluding model methods
            for meta_field in objects.model._meta.fields:

                if meta_field.name == fields[0]:

                    only_fields.append(specified_field)

            # Set `select_related` for related fields
            if len(fields) > 1:
                select_related.append('__'.join(fields[0:len(fields) - 1]))

        if len(only_fields):
            objects = objects.only(*only_fields)

        if len(self._meta.excludes):
            objects = objects.defer(*self._meta.excludes)

        if len(select_related):
            objects = objects.select_related(*select_related)

        if (has_m2m and not distinct) or distinct:
            objects = objects.distinct()

        return objects

    def full_dehydrate(self, bundle, for_list=False):

        """
        This override disables `full=True` and other things we don't use
        """

        # call the base class if qs param `fields` is not set
        if not len(self.specified_fields):
            return super(SpecifiedFields, self).full_dehydrate( \
                                                        bundle, for_list)

        # Dehydrate each field supplied in the `fields` parameter
        for field_name, field_object in self.fields.items():

            # A touch leaky but it makes URI resolution work.
            if getattr(field_object, 'dehydrated_type', None) == 'related':
                field_object.api_name = self._meta.api_name
                field_object.resource_name = self._meta.resource_name

            # Check for an optional method to do further dehydration.
            method = getattr(self, "dehydrate_%s" % field_name, None)

            if method:
                bundle.data[field_name] = method(bundle)

        bundle = self.dehydrate(bundle)
        return bundle

    def dehydrate(self, bundle):

        # Dehydrate each field including related ones
        for row in self.specified_fields:

            f = row.split('__')

            bundle.data[row] = reduce(getattr, f, bundle.obj)

            # display actual values for `choices` fields
            method = getattr(bundle.obj, "get_%s_display" % f[0], False)
            if method:
                bundle.data[f[0]] = method()
        return bundle

