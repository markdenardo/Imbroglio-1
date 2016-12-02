# Entity-Component architecture based loosely on JAForbes' idea:
# https://gist.github.com/JAForbes/99c15c0995b87a22b95a

world = 0
player = 1
monster = 2


class AspectType(type):
  
  def __new__(cls, name, bases, namespace):
    new_cls = super().__new__(cls, name, bases, namespace)
    if new_cls.root:
      new_cls.root.add_aspect(new_cls)
    return new_cls


class BaseAspect(metaclass=AspectType):
  domain = {}
  priority = 0
  root = None

  def __init__(self, *args):
    self.__dict__.update({k:v for k, v in self.root.items() if k in args})

  def setup(self):
    print("Setting up... " + str(self))
  
  def start(self):
    print("Starting... " + str(self))
    for uid in self._get_uids():
      self.run(uid)

  def run(self, uid):
    print("Running... " + str(self) + ": " + str(uid))

  def teardown(self):
    print("Tearing down... " + str(self))

  def _get_uids(self):
    if self.__dict__:
      return list(set.intersection(*[set(s) for s in self.__dict__.values()]))
    return list()


class Components(dict):
  def __init__(self, *args):

    class Aspect(BaseAspect):
      root = self

    super().__init__()
    self._aspects = list()
    for arg in args:
      self[arg] = _Entities()
    self.Aspect = Aspect

  def add_aspect(self, cls):
    self._aspects.append(cls(*cls.domain))
    self._aspects.sort(key=lambda x: x.priority)

  def run(self):
    for aspect in self._aspects:
      aspect.setup()
      aspect.start()
      aspect.teardown()


class _Entities(dict):
  def __init__(self):
    super().__init__()


component = Components("x", "y")
component["x"][player] = 1
component["y"][player] = 2
component["x"][monster] = 0


class Physics(component.Aspect):
  domain = {"x", "y"}
  
class Physics2(component.Aspect):
  domain = {"x", "y"}
  priority = -1


component.run()
