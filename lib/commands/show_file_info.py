from mutagen.id3 import ID3
import mutagen
import click
from lib.model.sermon import Sermon

@click.command()
@click.argument('filename')
def show_file_info(filename):
    print(filename)
    print()

    from mutagen.easyid3 import EasyID3
    print(EasyID3.valid_keys.keys())

    file_data = mutagen.File(filename)

    print("Technical Data")
    print("--------------")
    print(file_data.info.pprint())
    id3_data = ID3(filename)

    non_printable_tags = ['APIC:']

    print()
    print("Raw ID3 Tags")
    print("------------")
    printable_id3_tags = [key for key in id3_data.keys() if key not in non_printable_tags]

    for printable_tag in printable_id3_tags:
        print("{} : \"{}\"".format(printable_tag, id3_data[printable_tag]))

    for non_printable_tag in non_printable_tags:
        if non_printable_tag in list(id3_data.keys()):
            print("{}: NOT PRINTABLE".format(non_printable_tag))

    sermon = Sermon(filename)
    print()
    print("Sermon Mapping")
    print("--------------")
    print(sermon)
    print()