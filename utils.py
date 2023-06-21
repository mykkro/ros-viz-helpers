from pathlib import Path
from rosbags.highlevel import AnyReader
from rosbags.typesys import get_types_from_msg, register_types


def guess_msgtype(path: Path) -> str:
    """Guess message type name from path."""
    name = path.relative_to(path.parents[2]).with_suffix('')
    if 'msg' not in name.parts:
        name = name.parent / 'msg' / name.name
    return str(name)


def register_custom_types(msgpaths):
    add_types = {}

    for pathstr in msgpaths:
        msgpath = Path(pathstr)
        msgdef = msgpath.read_text(encoding='utf-8')
        add_types.update(get_types_from_msg(msgdef, guess_msgtype(msgpath)))

    register_types(add_types)
