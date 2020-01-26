
from command_registry import CommandRegistry

from .add_frame import AddFrame
from .add_universal_axis import AddUniversalAxis

main_toolbar = CommandRegistry()
main_toolbar.register('AddFrame', AddFrame())
main_toolbar.register('AddUniversalAxis', AddUniversalAxis())
