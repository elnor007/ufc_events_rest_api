from event_finding_util import findNext, findPrev, get_all_competitions_sorted, app
from flask import render_template, request


@app.route('/', methods=["GET", "POST"])
def home():
        if request.method == "POST":
                event_type = request.form.get("event_type")  # "previous" or "future"
                num_events = int(request.form.get("num_events"))
                
                if event_type == "previous":
                        events = findPrev(num_events)
                else:
                        events = findNext(num_events)

                return render_template("results.html", events=events)

        return render_template("home.html")
	


@app.route('/compData')
def compData():
	comps = get_all_competitions_sorted()
	return [comp["comp"] for comp in comps][::-1]



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80)

