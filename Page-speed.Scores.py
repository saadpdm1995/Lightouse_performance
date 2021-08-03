import requests
import json

# Documentation: https://developers.google.com/speed/docs/insights/v5/get-started

# JSON paths: https://developers.google.com/speed/docs/insights/v4/reference/pagespeedapi/runpagespeed

# Populate 'pagespeed.txt' file with URLs to query against API.
with open('pagespeed.txt') as pagespeedurls:
    download_dir = 'pagespeed-results-Scores.csv'
    file = open(download_dir, 'w')
    content = pagespeedurls.readlines()
    content = [line.rstrip('\n') for line in content]
    columnTitleRow = "URL, performance, acc, best-practices, seo, pwa\n"
    file.write(columnTitleRow)

    # This is the google pagespeed api url structure, using for loop to insert each url in .txt file
    for line in content:
        # If no "strategy" parameter is included, the query by default returns desktop data.
        x = f'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={line}&strategy=desktop&category=performance&category=pwa&category=best-practices&category=accessibility&category=SEO'
        print(f'Requesting {x}...')
        r = requests.get(x)
        final = r.json()
        # get elements from the JSON response
        try:
            urlid = final['id']
            split = urlid.split('?')  # This splits the absolute url from the api key parameter
            urlid = split[0]  # This reassigns urlid to the absolute url
            ID = f'URL ~ {urlid}'
            ID2 = str(urlid)
            urlperf = final['lighthouseResult']['categories']['performance']['score']
            FPerf = f'performance ~ {str(urlperf)}'
            FPerf2 = str(urlperf)
            urlacc = final['lighthouseResult']['categories']['accessibility']['score']
            Facc = f'accessibility ~ {str(urlacc)}'
            Facc2 = str(urlacc)
            urlbp = final['lighthouseResult']['categories']['best-practices']['score']
            Fbp = f'best-practices ~ {str(urlbp)}'
            Fbp2 = str(urlbp)
            urlseo = final['lighthouseResult']['categories']['seo']['score']
            Fseo = f'seo ~ {str(urlseo)}'
            Fseo2 = str(urlseo)
            urlpwa = final['lighthouseResult']['categories']['pwa']['score']
            Fpwa = f'pwa ~ {str(urlpwa)}'
            Fpwa2 = str(urlpwa)
        except KeyError:
            print(f'<KeyError> One or more keys not found {line}.')

        try:
            row = f'{urlid},{FPerf2},{Facc2},{Fbp2},{Fseo2},{Fpwa2}\n'
            file.write(row)
        except NameError:
            print(f'<NameError> Failing because of KeyError {line}.')
            file.write(f'<KeyError> & <NameError> Failing because of nonexistant Key ~ {line}.' + '\n')

        try:
            print(FPerf)
            print(Facc)
            print(Fbp)
            print(Fseo)
            print(Fpwa)
        except NameError:
            print(f'<NameError> Failing because of KeyError {line}.')

    file.close()