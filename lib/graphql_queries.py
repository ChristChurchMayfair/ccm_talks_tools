def find_sermon_by_url():
    return '''
    query ($url:String!) {
        Sermon(url: $url) {
            name,
            id,
            url,
            passage,
            series { name },
            speakers { name },
            event { name },
            duration,
            preachedAt
        }
    }
    '''

def find_series_by_name():
    return '''
    query ($name:String!) {
        Sermon(name: $name) {
            name,
            subtitle
            id,
            image3x2Url
        }
    }
    '''

def create_series_query():
    return '''
    mutation(
  $name: String!,
  $subtitle:String!,
  $image3x2Url:String
) {
    createSeries (
      name: $name,
      subtitle: $subtitle,
      image3x2Url: $image3x2Url
    ) {
      id
    }
}
    '''

def list_sermons():
    return '''
    query($number:Int!) {
        allSermons(last: $number, orderBy:preachedAt_ASC) {
            name,
            id,
            url,
            passage,
            series { id, name },
            speakers { id, name },
            event { id, name },
            duration,
            preachedAt
        }
    }
    '''

def create_sermon():
    return '''
    mutation(
  $name: String!,
  $url:String!,
  $duration:Int!,
  $preachedAt:DateTime!,
  $passage:String!
  $series_id:ID!,
  $speaker_ids:[ID!],
  $event_id:ID!
) {
    createSermon (
      name: $name,
      url: $url,
      duration: $duration,
      preachedAt: $preachedAt,
      passage: $passage,
      seriesId: $series_id,
      speakersIds: $speaker_ids,
      eventId: $event_id
    ) {
      id
    }
}
    '''

def delete_sermon():
    return '''
    mutation ($id: ID!) {
        deleteSermon(id: $id) {
            id
            name
        }
    }
    '''


def find_sermons_with_url_ending():
    return '''
    query($url_ends_with: String) {
      allSermons(filter: {
        OR: [{
          url_ends_with: $url_ends_with
        }]
      }) {
        id, name, url
      }
    }
    '''


def find_series_by_name():
    return '''
    query($name:String!) {
        Series(name: $name) {
            name,
            id
        }
    }
    '''

def find_speaker_by_name():
    return '''
    query($name:String!) {
        Speaker(name: $name) {
            name,
            id
        }
    }
    '''

def find_event_by_name():
    return '''
    query($name:String!) {
        Event(name: $name) {
            name,
            id
        }
    }
    '''

def list_series():
    return '''
   query($number:Int!) {
        allSeries(last: $number) {
            name,
            id,
            subtitle,
            image3x2Url
            sermons {
                id,
                preachedAt
            }
        }
    }
    '''

def list_speakers():
    return '''
   query($number:Int!) {
        allSpeakers(last: $number) {
            name,
            id,
            sermons {
                id,
                preachedAt
            }
        }
    }
    '''

def list_events():
    return '''
   query($number:Int!) {
        allEvents(last: $number) {
            name,
            id,
            sermons {
                id,
                preachedAt
            }
        }
    }
    '''