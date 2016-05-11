import SimPEG
from SimPEG import sp

class BaseRx(SimPEG.Survey.BaseRx):
    """
    Frequency domain receiver base class

    :param numpy.ndarray locs: receiver locations (ie. :code:`np.r_[x,y,z]`)
    :param string orientation: receiver orientation 'x', 'y' or 'z'
    :param string component: real or imaginary component 'real' or 'imag'
    """

    def __init__(self, locs, orientation=None, component=None):
        assert(orientation in ['x','y','z']), "Orientation %s not known. Orientation must be in 'x', 'y', 'z'. Arbitrary orientations have not yet been implemented."%orientation
        assert(component in ['real', 'imag']), "'component' must be 'real' or 'imag', not %s"%component

        self.projComp = orientation
        self.component = component

        SimPEG.Survey.BaseRx.__init__(self, locs, rxType=None) #TODO: remove rxType from baseRx

    def projGLoc(self, u):
        """Grid Location projection (e.g. Ex Fy ...)"""
        return u._GLoc(self.projField) + self.projComp

    def eval(self, src, mesh, f):
        """
        Project fields to recievers to get data.

        :param Source src: FDEM source
        :param Mesh mesh: mesh used
        :param Fields f: fields object
        :rtype: numpy.ndarray
        :return: fields projected to recievers
        """

        P = self.getP(mesh, self.projGLoc(f))
        f_part_complex = f[src, self.projField]
        f_part = getattr(f_part_complex, self.component) # get the real or imag component

        return P*f_part

    def evalDeriv(self, src, mesh, f, v, adjoint=False):
        """
        Derivative of projected fields with respect to the inversion model times a vector.

        :param Source src: FDEM source
        :param Mesh mesh: mesh used
        :param Fields f: fields object
        :param numpy.ndarray v: vector to multiply
        :rtype: numpy.ndarray
        :return: fields projected to recievers
        """

        P = self.getP(mesh, self.projGLoc(f))

        if not adjoint:
            Pv_complex = P * v
            Pv = getattr(Pv_complex, self.component)
        elif adjoint:
            Pv_real = P.T * v

            if self.component == 'imag':
                Pv = 1j*Pv_real
            elif self.component == 'real':
                Pv = Pv_real.astype(complex)
            else:
                raise NotImplementedError('must be real or imag')

        return Pv


class eField(BaseRx):
    """
    Electric field FDEM receiver

    :param numpy.ndarray locs: receiver locations (ie. :code:`np.r_[x,y,z]`)
    :param string orientation: receiver orientation 'x', 'y' or 'z'
    :param string component: real or imaginary component 'real' or 'imag'
    """

    def __init__(self, locs, orientation=None, component=None):
        self.projField = 'e'
        BaseRx.__init__(self, locs, orientation, component)


class bField(BaseRx):
    """
    Magnetic flux FDEM receiver

    :param numpy.ndarray locs: receiver locations (ie. :code:`np.r_[x,y,z]`)
    :param string orientation: receiver orientation 'x', 'y' or 'z'
    :param string component: real or imaginary component 'real' or 'imag'
    """

    def __init__(self, locs, orientation=None, component=None):
        self.projField = 'b'
        BaseRx.__init__(self, locs, orientation, component)


class hField(BaseRx):
    """
    Magnetic field FDEM receiver

    :param numpy.ndarray locs: receiver locations (ie. :code:`np.r_[x,y,z]`)
    :param string orientation: receiver orientation 'x', 'y' or 'z'
    :param string component: real or imaginary component 'real' or 'imag'
    """

    def __init__(self, locs, orientation=None, component=None):
        self.projField = 'h'
        BaseRx.__init__(self, locs, orientation, component)


class jField(BaseRx):
    """
    Current density FDEM receiver

    :param numpy.ndarray locs: receiver locations (ie. :code:`np.r_[x,y,z]`)
    :param string orientation: receiver orientation 'x', 'y' or 'z'
    :param string component: real or imaginary component 'real' or 'imag'
    """

    def __init__(self, locs, orientation=None, component=None):
        self.projField = 'j'
        BaseRx.__init__(self, locs, orientation, component)
