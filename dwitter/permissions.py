class IsAuthorOrReadOnly():
    # Extension: permissions.BasePermission

    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        # permissions.SAFE_METHODS
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.author == request.user
