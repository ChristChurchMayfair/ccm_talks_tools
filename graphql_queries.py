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


def create_sermon():
    return '''
    mutation {
        createSermon(
            name: $name,
            preachedAt: $preachedAt,
            duration: $duration,
            passage: $passage,
            url: $url)
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