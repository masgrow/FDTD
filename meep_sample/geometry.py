from meep import Vector3, Sphere


def particle(**kwargs):
    def xyz_length(rad, pml, pad):
        return 2 * (rad + pml + pad)

    def cell():
        return Vector3(xyz_length(kwargs['rad'], kwargs['pml'], kwargs['pad']),
                       xyz_length(kwargs['rad'], kwargs['pml'], kwargs['pad']),
                       xyz_length(kwargs['rad'], kwargs['pml'], kwargs['pad']))

    def part():
        return Sphere(radius=kwargs['rad'], material=kwargs['mat'], center=Vector3(0, 0, 0))

    if kwargs['geom'] == 'part':
        if kwargs['cell']:
            return cell()

        elif not kwargs['cell']:
            return [part()]


def cylinder(**kwarg):
    def xyz_length(rad, hg, pml, pad):
        return

    def cell():
        return Vector3