from app import app
from app.forms.home_page_search import HomePageSearch
from app.forms.structured_search_form import StructuredSearch
import re
from flask import render_template, request, redirect, url_for, make_response
from content.recent_judgments import recent_judgments
from content.service_wide import service
from content.search_results import search_results
from content.courts import courts
from content.disambiguation_results import disambiguation_results


@app.route('/')
def home():
    form = HomePageSearch()

    return render_template(
        'home.html',
        service=service,
        recent_judgments=recent_judgments,
        courts=courts,
        form=form
    )


@app.route('/results', methods=['GET'])
def results():
    form = StructuredSearch(request.args)

    search_term = request.args['search_term']

    # User checked the neutral citation field
    if form.neutral_citation.data:
        return render_template(
            'disambiguation.html',
            service=service,
            search_results=disambiguation_results,
            form=form
        )

    # Matches the neutral citation regex
    if re.match(r'^\[?\d{4}\]?\s\w{4,5}\s?(\d{2,4}|\w{3,4})\s?', search_term):
        return render_template(
            'disambiguation.html',
            service=service,
            search_results=disambiguation_results,
            form=form,
            show_neutral_citation_check=True
        )

    return render_template(
        'results.html',
        service=service,
        search_results=search_results,
        form=form
    )


@app.route('/terms-of-use')
def terms_of_use():
    return render_template(
        'terms_of_use.html',
        service=service,
    )


@app.route('/disambiguation/')
def disambiguation():
    return render_template(
        'disambiguation.html',
        service=service,
        neutral_citation=request.args['neutral_citation']
    )


@app.route('/no-results/')
def no_results():
    return render_template(
        'no_results.html',
        service=service,
        search_term=request.args['search_term']
    )


@app.route('/open-justice-licence')
def open_justice_licence():
    return render_template(
        'open_justice_licence.html',
        service=service,
    )


@app.route('/judgment')
def judgment_quick_route():
    return redirect(url_for('judgment'))


@app.route('/ewhc/admin/2021/3290')
def judgment():
    resp = make_response(render_template('judgment.html'))
    resp.headers['Content-Security-Policy'] = "script-src 'nonce-2wCEAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRo' " \
                                              "'strict-dynamic' " \
                                              "'unsafe-inline' " \
                                              "https:;" \
                                              "object-src 'none';" \
                                              "base-uri 'none';"
    return resp


@app.route('/search')
def structured_search():
    form = StructuredSearch()

    return render_template(
        'structured_search.html',
        service=service,
        form=form
    )
