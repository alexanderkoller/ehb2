
from __init__ import *
from tables import *
from itertools import groupby
from helpers import *
from flask import request


@app.route("/show-participants.html")
def show_participants():
    participants = session.query(Participant).all()
    paid_participants = session.query(Participant).filter(Participant._paypal_status == 5)
    total_donations = sum([p.donation for p in participants])

    return render_template("show_participants.html", title="Show participants",
                           participants=participants, total_donations=total_donations,
                           part_data=make_part_data(paid_participants), country_data=make_country_data(paid_participants))

@app.route("/show-participant.html")
def show_participant():
    id = int(request.args.get('id'))
    participant = session.query(Participant).filter(Participant.id == id).first()
    payment_steps = session.query(PaypalHistory).filter(PaypalHistory.participant_id == id).\
        filter(PaypalHistory.payment_step == 1).order_by(PaypalHistory.timestamp).all()
    ps = [(id, p.shortname()) for (id,p) in sorted(paypal_statuses.items())]

    return render_template("show_participant.html", title="Participant details", data=participant, paypal_history=payment_steps,
                           paypal_statuses=ps)





part_colors = ["428BCA", "5CB85C", "F0AD4E", "D9534F"]
part_highlight_colors = ["5DA6E6", "78D077", "FCC671", "E16864"]

country_colors = ["42847D", "615192", "D4C26A", "D4976A", "428BCA", "5CB85C", "F0AD4E", "D9534F"]
country_highlight_colors = ["6A9E99", "887CAF", "FFF0AA", "FFCEAA", "5DA6E6", "78D077", "FCC671", "E16864"]


def participants_by(all_participants, fn):
    s = sorted(all_participants, key=fn)
    return groupby(s, fn)


def make_part_data(all_participants):
    p_by_part = participants_by(all_participants, lambda p: p.part1)
    return ["{ value: %d, color:'#%s', highlight:'#%s', label:'%s'}" %
            (len(list(people)), part_colors[i], part_highlight_colors[i], lparts[part])
            for (i, (part,people)) in enumerate(p_by_part)]


def make_country_data(all_participants):
    p_by_country = participants_by(all_participants, lambda p: p.country.id)
    return ["{ value: %d, color:'#%s', highlight:'#%s', label:'%s'}" %
            (len(list(people)), country_colors[i], country_highlight_colors[i], countries[country].name_en)
            for (i, (country,people)) in enumerate(p_by_country)]

