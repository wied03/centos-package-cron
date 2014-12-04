from rpmUtils.miscutils import splitFilename

class PackageParser:
    @staticmethod
    def parsePackage(filename):
        (n, v, r, e, a) = splitFilename(filename)
        return {
        'name':n,
        'version':v,
        'release':r,
        'arch':a
        }
    