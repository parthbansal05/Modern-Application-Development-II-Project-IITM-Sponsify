import json
import os
import math
from datetime import timedelta
from datetime import datetime
import time

from flask import flash, redirect, render_template, send_file, session, url_for, request, abort, jsonify
from flask_bcrypt import check_password_hash


from sqlalchemy.exc import IntegrityError

import server_pkg.essentials as e
from server_pkg.server.app import bcrypt, create_app, db
from server_pkg.server.forms import login_form, register_form_inf, register_form_spo, create_campaign_form, register_form_usr
from server_pkg.server.models import User
from server_pkg.server_db_manager import DB_Manager
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request



def server(app, socketio):

    @app.before_request
    def session_handler():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=60)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    @app.template_filter('timestamp_to_datetime')
    def timestamp_to_datetime_filter(s):
        return datetime.fromtimestamp(int(s)).strftime('%Y-%m-%d %H:%M:%S')
    
    @app.template_filter('timestamp_to_date')
    def timestamp_to_date_filter(s):
        return datetime.fromtimestamp(int(s)).strftime('%Y-%m-%d')
    
    @app.template_filter('unique_list')
    def unique_list_filter(l):
        return list(set(l))
    
    def get_jwt_id():
        verify_jwt_in_request(optional = True)
        return get_jwt_identity()

    # user authentication
    @app.route("/login", methods=["POST"], strict_slashes=False)
    def login():
        if request.method == 'POST':
            data = request.json
            email = data.get('email')
            pwd = data.get('pwd')
            next_url = data.get('next')

            user = User.query.filter_by(email=email).first()

            if check_password_hash(user.pwd, pwd):
                redirect_url = ""
                print(user.user_type)
                print(type(next_url))
                # if user.user_type == "A":
                #     redirect_url = url_for('admin')
                # elif user.user_type == "S":
                #     redirect_url = url_for('sponsor')
                # elif user.user_type == "I":
                #     redirect_url = url_for('influencer')
                # elif user.user_type == "U":
                #     redirect_url = url_for('user')
                
                access_token = create_access_token(identity=user.id, expires_delta = False)
                
                if next_url == "None" or next_url == None:
                    return jsonify(access_token=access_token, redirect_url = redirect_url)
                
                if not e.is_safe_url(next_url):
                    return jsonify({"msg": "Bad URL"}), 400
                
                return jsonify(access_token=access_token, redirect_url = next_url)
            else:
                return jsonify({"msg": "Wrong username or password"}), 401


    @app.route("/influencer/register", methods=["POST"], strict_slashes=False)
    def influencer_register():
        if request.method == 'POST':
            data = request.json
            username = data.get('username')
            email = data.get('email')
            pwd = data.get('pwd')
            ph_no = data.get('phno')
            category = data.get('category')
            niche = data.get('niche')
            next_url = data.get('next')
            user_type = "I"
            print(data)
            try:
                newuser = User(
                    username=username,
                    email=email,
                    ph_no=ph_no,
                    pwd=bcrypt.generate_password_hash(pwd),
                    user_type=user_type,
                    category=category,
                    niche=niche,
                    followers=0,
                    industry="",
                    budget=0)
                
                db.session.add(newuser)
                db.session.commit()
                return jsonify({"msg": "Account Successfully created"}), 200
            except IntegrityError as exc:
                db.session.rollback()
                return jsonify({"error": "User already exists!"}), 409
            except Exception as exc:
                db.session.rollback()
                return jsonify({"error": "Something went wrong!"}), 500
    
    @app.route("/sponsor/register", methods=["POST"], strict_slashes=False)
    def sponsor_register():
        if request.method == 'POST':
            data = request.json
            username = data.get('username')
            email = data.get('email')
            pwd = data.get('pwd')
            ph_no = data.get('phno')
            industry = data.get('industry')
            next_url = data.get('next')
            user_type = "S"
            print(data)
            try:
                newuser = User(
                    username=username,
                    email=email,
                    ph_no=ph_no,
                    pwd=bcrypt.generate_password_hash(pwd),
                    user_type=user_type,
                    category="",
                    niche="",
                    followers=0,
                    industry=industry,
                    budget=0)
                
                db.session.add(newuser)
                db.session.commit()
                return jsonify({"msg": "Account Successfully created"}), 200
            except IntegrityError as exc:
                db.session.rollback()
                return jsonify({"error": "User already exists!"}), 409
            except Exception as exc:
                db.session.rollback()
                return jsonify({"error": "Something went wrong!"}), 500


    @app.route("/user/register", methods=("GET", "POST"), strict_slashes=False)
    def user_register():
        if request.method == 'POST':
            data = request.json
            username = data.get('username')
            email = data.get('email')
            pwd = data.get('pwd')
            ph_no = data.get('phno')
            industry = data.get('industry')
            next_url = data.get('next')
            user_type = "U"
            print(data)
            try:
                newuser = User(
                    username=username,
                    email=email,
                    ph_no=ph_no,
                    pwd=bcrypt.generate_password_hash(pwd),
                    user_type=user_type,
                    category="",
                    niche="",
                    followers=0,
                    industry="",
                    budget=0)
                db.session.add(newuser)
                db.session.commit()
                return jsonify({"msg": "Account Successfully created"}), 200
            except IntegrityError as exc:
                db.session.rollback()
                return jsonify({"error": "User already exists!"}), 409
            except Exception as exc:
                db.session.rollback()
                return jsonify({"error": "Something went wrong!"}), 500

    @e.admin_required
    @app.route("/delete_user/<uid>", methods=["GET"], strict_slashes=False)
    def users_delete(uid):
        uid = int(uid)
        try:
            user_details = User.query.filter_by(id=uid).first()
            # check it user exists
            if not user_details:
                raise Exception("User does not exist")
        except Exception as exc:
            print(exc)
            return jsonify({"error": "User does not exist"}), 404
        
        try:
            if uid == 1:
                raise Exception("Cannot delete admin")
            if uid == get_jwt_id():
                raise Exception("Cannot delete yourself")
            if User.query.filter_by(id=uid).first().user_type == "A":
                raise Exception("Cannot delete admin")
            if User.query.filter_by(id=uid).first().user_type == "S":
                if DB_Manager().RemoveSponsorCampaigns(uid):
                    pass
                if DB_Manager().RemoveSponsorAdRequest(uid):
                    pass
            if User.query.filter_by(id=uid).first().user_type == "I":
                if DB_Manager().RemoveInfluencerAdRequest(uid):
                    pass
            User.query.filter_by(id=uid).delete()
            db.session.commit()
            return jsonify({"status": "Deleted"}), 200
        except Exception as exc:
            print(exc)
            return jsonify({"error": str(exc)}), 500

    # # content page
    # @app.route("/", methods=["GET"], strict_slashes=False)
    # def index():       
    #     if not current_user.is_authenticated:
    #         return redirect(url_for('login'))    
    #     if current_user.user_type == "A":
    #         redirect_url = url_for('admin_dashboard')
    #     elif current_user.user_type == 'S':
    #         redirect_url = url_for('sponsor_dashboard')
    #     elif current_user.user_type == "I":
    #         redirect_url = url_for('influencer_dashboard')
    #     elif current_user.user_type == "U":
    #         redirect_url = url_for('user_dashboard')
    #     return redirect(redirect_url)
    
    # admin pages
    @app.route("/admin/dashboard", methods=["GET"], strict_slashes=False)
    @e.admin_required
    def admin_dashboard():
        userID = get_jwt_id()
        campaigns = DB_Manager().QueryRecentCampaigns()
        
        influencer = ([[inf.id, inf.username, inf.email, inf.ph_no, inf.user_type, inf.category, inf.niche, inf.followers, inf.industry, inf.budget] for inf in User.query.filter(User.user_type == "I").all()])
        sponsors = ([[spo.id, spo.username, spo.email, spo.ph_no, spo.user_type, spo.category, spo.niche, spo.followers, spo.industry, spo.budget] for spo in User.query.filter(User.user_type == "S").all()])        
        users = ([[usr.id, usr.username, usr.email, usr.ph_no, usr.user_type, usr.category, usr.niche, usr.followers, usr.industry, usr.budget] for usr in User.query.filter(User.user_type == "U").all()])
        
        camps = DB_Manager().QueryCampaignTitleID()
        camp_dict = {camps[0][i]: camps[1][i] for i in range(len(camps[0]))} if camps not in [None, []] else {}

        return jsonify(campaigns=campaigns,
                        users=users,
                        influencer=influencer,
                        sponsors=sponsors,
                        camp_dict=camp_dict,
                        admin_email=str(User.query.filter_by(id=userID).first().email),
                        admin_phno=str(User.query.filter_by(id=userID).first().ph_no))

    @app.route("/admin/insights", methods=["GET"], strict_slashes=False)
    @e.admin_required
    def admin_insights():
        flagged_stats =DB_Manager().QueryFlaggedCampaignsStats()
        visibility_stats =DB_Manager().QueryCampaignsVisibilityStats()

        # user_type_mapping = {'S': 'Sponsor', 'I': 'Influencer', 'A': 'Admin', 'U': 'User'}
        user_counts = {'S': 0, 'I': 0, 'A': 0, 'U': 0}
        for user_type, count in User.query.with_entities(User.user_type, db.func.count(User.user_type)).group_by(User.user_type).order_by(User.user_type.desc()).all():
            user_counts[user_type] = count

        top5_influencers = User.query.filter_by(user_type="I").order_by(User.followers.desc()).limit(5).all()
        Approved_stats = DB_Manager().QueryCampaignsAcceptanceStatus()


        flagged_campaigns_stats = [{'number': flagged_stats[0], 'label': "number_of_flagged_campaigns"},
                                    {'number': flagged_stats[1], 'label': "number_of_non_flagged_campaigns"}]
        visibility_campaigns_stats = [{'number': visibility_stats[0], 'label': "Public"},
                                    {'number': visibility_stats[1], 'label': "Private"}]
        Approved_campaigns_stats = [{'number': Approved_stats[0][0], 'label': "Approved"},
                                    {'number': Approved_stats[1][0], 'label': "Rejected"},
                                    {'number': Approved_stats[2][0], 'label': "PENDING"}]
        
        

        user_distribution = [
            {'number': user_counts['U'], 'label': "User"},
            {'number': user_counts['S'], 'label': "Sponsor"},
            {'number': user_counts['I'], 'label': "Influencer"},
            {'number': user_counts['A'], 'label': "Admin"}
        ]
        influencer_stats = [{'number': top5_influencers[i].followers, 'label': top5_influencers[i].username} for i in range(min(len(top5_influencers), 5))]
        info = [flagged_campaigns_stats, visibility_campaigns_stats, user_distribution, influencer_stats, Approved_campaigns_stats]
        return jsonify(info=info)

    @app.route("/admin/view_campaign/<cid>", methods=["GET"], strict_slashes=False)
    @e.admin_required
    def admin_view_campaign(cid):
        cid = int(cid)
        campaign = DB_Manager().QueryCampaignByCID(cid)
        sponsors = ([[spo.id, spo.username, spo.email, spo.ph_no, spo.user_type, spo.category, spo.niche, spo.followers, spo.industry, spo.budget] for spo in User.query.filter(User.user_type == "S").all()])        
        return jsonify(campaign=campaign,
                       sponsors=sponsors)
    
    @app.route("/admin/view_all_campaigns", methods=["GET"], strict_slashes=False)
    @e.admin_required
    def admin_view_all_campaigns():
        campaigns=DB_Manager().QueryAllCampaigns()
        sponsors = ([[spo.id, spo.username, spo.email, spo.ph_no, spo.user_type, spo.category, spo.niche, spo.followers, spo.industry, spo.budget] for spo in User.query.filter(User.user_type == "S").all()])        
        return jsonify(campaigns=campaigns,
                          sponsors=sponsors)
    
    @app.route("/admin/flag_campaign/<cid>", methods=["GET"], strict_slashes=False)
    @e.admin_required
    def admin_flag_campaign(cid):
        cid = int(cid)
        if DB_Manager().flagCampaign(cid):
            return jsonify({"msg": "Campaign flagged"}), 200
        else:
            return jsonify({"error": "Failed to flag campaign"}), 500
    
    @app.route("/admin/unflag_campaign/<cid>", methods=["GET"], strict_slashes=False)
    @e.admin_required
    def admin_unflag_campaign(cid):
        cid = int(cid)
        if DB_Manager().unflagCampaign(cid):
            return jsonify({"msg": "Campaign unflagged"}), 200
        else:
            return jsonify({"error": "Failed to unflag campaign"}), 500

    # # sponsor pages
    @app.route("/sponsor/dashboard", methods=["GET"], strict_slashes=False)
    @e.sponsor_required
    def sponsor_dashboard():
        userID = get_jwt_id()
        campaigns = DB_Manager().QueryCampaignBySID(userID)
        spo = User.query.filter_by(id=userID).first()
        sponsors = ([spo.id, spo.username, spo.email, spo.ph_no, spo.user_type, spo.category, spo.niche, spo.followers, spo.industry, spo.budget])
        return jsonify(campaigns=campaigns,
                       info = sponsors)        
    
    @app.route("/sponsor/update_dashboard", methods=("GET", "POST"), strict_slashes=False)
    @e.sponsor_required
    def sponsor_update_dashboard():
        userID = get_jwt_id()
        user = User.query.filter_by(id=userID).first()
        if request.method == 'POST':
            print("inpost")
            data = request.json
            username = data.get('username')
            pwd = data.get('pwd')
            ph_no = data.get('phno')
            industry = data.get('industry')
            next_url = data.get('next')
            try:

                user.pwd = bcrypt.generate_password_hash(pwd)
                user.username = username
                user.ph_no = ph_no
                user.industry = industry

                db.session.commit()
                return jsonify({"msg": "Details updated"}), 200
            except Exception as exc:
                print(exc)
                db.session.rollback()
                return jsonify({"error": "Failed to update details"}), 500
        
        elif request.method == 'GET':
            return jsonify(email=user.email,
                           username=user.username,
                           ph_no=user.ph_no,
                           industry=user.industry)
  
    @app.route("/sponsor/set_visibility/<cid>/<visibility>", methods=["GET"], strict_slashes=False)
    @e.sponsor_required
    def sponsor_set_visibility(cid, visibility):
        cid = int(cid)
        if DB_Manager().SetCampaignVisibility(cid, visibility):
            return jsonify({"msg": "Visibility set"}), 200
        else:
            return jsonify({"error": "Failed to set visibility"}), 500

    
    # @app.route("/sponsor/view_campaigns/<cid>", methods=["GET"], strict_slashes=False)
    # @e.sponsor_required
    # def sponsor_view_campaigns(cid):
    #     cid = int(cid)
    #     campaign = DB_Manager().QueryCampaignByCID(cid)
    #     return render_template("sponsor/sponsor_view_campaign.html",
    #                            text="Sponsor View Campaigns",
    #                            title="Sponsor View Campaigns",
    #                            campaign=campaign,
    #                            btn_action="Sponsor View Campaigns")
    
    # @app.route("/sponsor/create_campaign", methods=["GET", "POST"], strict_slashes=False)
    # @e.sponsor_required
    # def sponsor_create_campaign():
    #     form = create_campaign_form()
    #     if form.validate_on_submit():
    #         try:
    #             title = form.title.data
    #             description = form.description.data
    #             sdate = time.mktime(time.strptime(str(form.sdate.data), "%Y-%m-%d"))
    #             edate = time.mktime(time.strptime(str(form.edate.data), "%Y-%m-%d"))
    #             budget = form.budget.data
    #             visibility = form.visibility.data
    #             goal = form.goal.data
    #             flagged = "NO"
    #             SID = current_user.get_id()
                
    #             if DB_Manager().AddCampaigns(SID, title, description, sdate, edate, budget, visibility, goal, flagged):
    #                 flash("Campaign created", "success")
    #             else:
    #                 flash("Failed to create campaign1", "danger")
    #         except Exception as exc:
    #             print(exc)
    #             flash("Failed to create campaign2", "danger")
    #     return render_template("sponsor/create_campaign.html",
    #                            form=form,
    #                            text="Sponsor Create Campaign",
    #                            title="Sponsor Create Campaign",
    #                            btn_action="Create Campaign")

    # @app.route("/sponsor/update_campaign/<cid>", methods=["GET", "POST"], strict_slashes=False)
    # @e.sponsor_required
    # def sponsor_update_campaign(cid):
    #     cid = int(cid)
    #     form = create_campaign_form()
    #     campaign = DB_Manager().QueryCampaignByCID(cid)
    #     if form.validate_on_submit():
    #         try:
    #             title = form.title.data
    #             description = form.description.data
    #             sdate = time.mktime(time.strptime(str(form.sdate.data), "%Y-%m-%d"))
    #             edate = time.mktime(time.strptime(str(form.edate.data), "%Y-%m-%d"))
    #             budget = form.budget.data
    #             visibility = form.visibility.data
    #             goal = form.goal.data
                
    #             if DB_Manager().UpdateCampaigns(cid, title, description, sdate, edate, budget, visibility, goal):
    #                 flash("Campaign updated", "success")
    #             else:
    #                 flash("Failed to update campaign1", "danger")
    #         except Exception as exc:
    #             print(exc)
    #             flash("Failed to update campaign2", "danger")
    #         return redirect(url_for('sponsor_update_campaign', cid=cid))
        
    #     form.title.data = campaign[2][0]
    #     form.description.data = campaign[3][0]
    #     form.sdate.data = datetime.fromtimestamp(campaign[4][0])
    #     form.edate.data = datetime.fromtimestamp(campaign[5][0])
    #     form.budget.data = campaign[6][0]
    #     form.visibility.data = campaign[7][0]
    #     form.goal.data = campaign[8][0]
    #     return render_template("sponsor/update_campaign.html",
    #                            form=form,
    #                            text="Sponsor Update Campaign",
    #                            title="Sponsor Update Campaign",
    #                            btn_action="Update Campaign")
    
    # @app.route("/sponsor/delete_campaign/<cid>", methods=["GET"], strict_slashes=False)
    # @e.sponsor_required
    # def sponsor_delete_campaign(cid):
    #     cid = int(cid)
    #     if DB_Manager().RemoveCampaign(cid):
    #         flash("Campaign deleted", "success")
    #     else:
    #         flash("Failed to delete campaign", "danger")
    #     return redirect(url_for('sponsor_dashboard'))

    # @app.route("/sponsor/inbox", methods=["GET"], strict_slashes=False)
    # @e.sponsor_required
    # def sponsor_inbox():
    #     userID = current_user.get_id()
    #     inbox = DB_Manager().QuerySponsorInBoxChatOverView(userID)
    #     camps = DB_Manager().QueryCampaignTitleID()
    #     camp_dict = {camps[0][i]: camps[1][i] for i in range(len(camps[0]))}
    #     return render_template("sponsor/sponsor_inbox.html",
    #                            text="Sponsor Inbox",
    #                            title="Sponsor Inbox",
    #                            influencers = User.query.filter(User.user_type == "I").all(),
    #                            inbox=inbox,
    #                            camp_dict = camp_dict,
    #                            btn_action="Sponsor Inbox")
    
    # @app.route("/sponsor/inbox/<iid>", methods=["GET", "POST"], strict_slashes=False)
    # @e.sponsor_required
    # def sponsor_inbox_chat(iid):
    #     userID = current_user.get_id()
    #     DB_Manager().updateAdRequestSeenSOPN(iid, userID)
    #     if request.method == "POST":
    #         try:
    #             msg = request.form["message"]
    #             campaign = request.form["campaign"]
    #             modified_budget = request.form["modified_budget"]
    #             modified_terms = request.form["modified_terms"]
    #             if msg == "" and modified_budget == "" and modified_terms == "": raise Exception("Empty message")
                
    #             if modified_budget == "": modified_budget = DB_Manager().QuerySponsorInBoxChatLastBudget(int(iid), userID, campaign)[0][0]
    #             if modified_terms == "": modified_terms = DB_Manager().QuerySponsorInBoxChatLastTerm(int(iid), userID, campaign)[0][0]

    #             DB_Manager().AddAdRequest(campaign, userID, iid, "SOPN", "PENDING", msg, modified_budget, modified_terms, "True", "False")
    #         except Exception as exc:
    #             print(exc)
    #             flash("Failed to send message", "danger")

    #     inbox = DB_Manager().QuerySponsorInBoxChat(userID, int(iid))
    #     camps = DB_Manager().QueryCampaignTitleID()
    #     camp_dict = {camps[0][i]: camps[1][i] for i in range(len(camps[0]))}
    #     return render_template("sponsor/sponsor_inbox_chat.html",
    #                         text="Sponsor Inbox",
    #                         title="Sponsor Inbox",
    #                         inbox=inbox,
    #                         camp_dict = camp_dict,
    #                         influencer = User.query.filter_by(id=iid).first(),
    #                         btn_action="Sponsor Inbox")
    
    # @app.route("/sponsor/accept_ad_request/<iid>/<sid>/<status>", methods=["GET"], strict_slashes=False)
    # @e.sponsor_required
    # def sponsor_accept_ad_request(iid, sid, status):
    #     cid = request.args.get('cid')  # Accessing cid as a query parameter
    #     print(iid, sid, status, cid)
    #     if DB_Manager().updateAdRequestStatus(iid, sid, status, cid):
    #         flash("Ad request accepted successfully", "success")
    #     else:
    #         flash("Failed to accept ad request", "danger")
    #     return redirect(url_for('sponsor_inbox_chat', iid=iid))
    
    # @app.route("/sponsor/search_influencer", methods=["GET"], strict_slashes=False)
    # @e.sponsor_required
    # def sponsor_search_influencer():
    #     userID = current_user.get_id()
    #     influencers = User.query.filter_by(user_type="I").all()
    #     campaigns = DB_Manager().QueryCampaignIDAndNameAndBudgetBySID(userID)

    #     return render_template("sponsor/sponsor_search_influencer.html",
    #                            text="Sponsor Search Influencer",
    #                            title="Sponsor Search Influencer",
    #                            influencers=influencers,
    #                            campaigns=campaigns,
    #                            btn_action="Sponsor Search Influencer")
    
    # @app.route("/sponsor/initiate_chat/<cid>/<iid>/<budget>", methods=["GET"], strict_slashes=False)
    # @e.sponsor_required
    # def sponsor_initiate_chat(cid, iid, budget):
    #     userID = current_user.get_id()
    #     msg = "Hi, would you like to collaborate on my campaign?"
    #     if DB_Manager().AddAdRequest(cid, userID, iid, "SOPN", "PENDING", msg, budget, "", "True", "False"):
    #         flash("Chat initiated successfully", "success")
    #     else:
    #         flash("Failed to initiate chat", "danger")
    #     return redirect(url_for('sponsor_search_influencer'))
    
    # @app.route("/influencer/dashboard", methods=["GET"], strict_slashes=False)
    # @e.influencer_required
    # def influencer_dashboard():
    #     userID = current_user.get_id()
    #     return render_template("influencer/influencer_dash.html",
    #                            text="Influencer Dashboard",
    #                            title="Influencer Dashboard",
    #                            info = User.query.filter_by(id=userID).first(),
    #                            btn_action="Influencer Dashboard")

    # @app.route("/influencer/dashboard/<iid>", methods=["GET"], strict_slashes=False)
    # @login_required
    # def influencer_dashboard_iid(iid):
    #     info = User.query.filter_by(id=iid).first()
    #     if info.user_type != "I":
    #         return render_template("404.html"), 404
    #     return render_template("influencer/influencer_dash.html",
    #                            text="Influencer Dashboard",
    #                            title="Influencer Dashboard",
    #                            info = info,
    #                            btn_action="Influencer Dashboard")
    
    # @app.route("/influencer/update_dashboard", methods=["GET", "POST"], strict_slashes=False)
    # @e.influencer_required
    # def influencer_update_dashboard():
    #     userID = current_user.get_id()
    #     user = User.query.filter_by(id=userID).first()
    #     form = register_form_inf()
    #     if form.validate_on_submit():
    #         try:
    #             pwd = form.pwd.data
    #             username = form.username.data
    #             ph_no = form.ph_no.data
    #             category = form.category.data
    #             niche = form.niche.data

    #             user.pwd = bcrypt.generate_password_hash(pwd)
    #             user.username = username
    #             user.ph_no = ph_no
    #             user.category = category
    #             user.niche = niche

    #             db.session.commit()
    #             flash("Details updated", "success")
    #         except Exception as exc:
    #             db.session.rollback()
    #             flash("Failed to update details", "danger")
    #         return redirect(url_for('influencer_update_dashboard'))
    #     form.email.data = user.email
    #     form.username.data = user.username
    #     form.ph_no.data = user.ph_no
    #     form.category.data = user.category
    #     form.niche.data = user.niche
    #     return render_template("influencer/influencer_update_dashboard.html",
    #                              form=form,
    #                              text="Influencer Update Dashboard",
    #                              title="Influencer Update Dashboard",
    #                              btn_action="Update Dashboard")

    # @app.route("/influencer/search_campaigns", methods=["GET"], strict_slashes=False)
    # @e.influencer_required
    # def influencer_search_campaigns():
    #     userID = current_user.get_id()
    #     campaigns = DB_Manager().QueryPublicCampaign()
    #     return render_template("influencer/influencer_search_campaigns.html",
    #                            text="Influencer Search Campaigns",
    #                            title="Influencer Search Campaigns",
    #                            campaigns=campaigns,
    #                            btn_action="Influencer Search Campaigns")
    
    # @app.route("/influencer/initiate_chat/<cid>/<sid>/<budget>", methods=["GET"], strict_slashes=False)
    # @e.influencer_required
    # def influencer_initiate_chat(cid, sid, budget):
    #     userID = current_user.get_id()
    #     msg = "Hi, I am interested in your campaign. Can we discuss more about it?"
    #     if DB_Manager().AddAdRequest(cid, sid, userID, "INFL", "PENDING", msg, budget, "", "False", "True"):
    #         flash("Chat initiated successfully", "success")
    #     else:
    #         flash("Failed to initiate chat", "danger")
    #     return redirect(url_for('influencer_search_campaigns'))
    
    # @app.route("/influencer/inbox", methods=["GET"], strict_slashes=False)
    # @e.influencer_required
    # def influencer_inbox():
    #     userID = current_user.get_id()
    #     inbox = DB_Manager().QueryInfluencerInBoxChatOverView(userID)
    #     camps = DB_Manager().QueryCampaignTitleID()
    #     camp_dict = {camps[0][i]: camps[1][i] for i in range(len(camps[0]))}
    #     return render_template("influencer/influencer_inbox.html",
    #                            text="Influencer Inbox",
    #                            title="Influencer Inbox",
    #                            sponsors = User.query.filter(User.user_type == "S").all(),
    #                            inbox=inbox,
    #                            camp_dict = camp_dict,
    #                            btn_action="Influencer Inbox")
    
    # @app.route("/influencer/inbox/<sid>", methods=["GET", "POST"], strict_slashes=False)
    # @e.influencer_required
    # def influencer_inbox_chat(sid):
    #     userID = current_user.get_id()
    #     DB_Manager().updateAdRequestSeenINFL(userID, sid)
    #     if request.method == "POST":
    #         try:
    #             msg = request.form["message"]
    #             campaign = request.form["campaign"]
    #             modified_budget = request.form["modified_budget"]
    #             modified_terms = request.form["modified_terms"]
    #             if msg == "" and modified_budget == "" and modified_terms == "": raise Exception("Empty message")
                
    #             if modified_budget == "": modified_budget = DB_Manager().QueryInfluencerInBoxChatLastBudget(userID, int(sid), campaign)[0][0]
    #             if modified_terms == "": modified_terms = DB_Manager().QueryInfluencerInBoxChatLastTerm(userID, int(sid), campaign)[0][0]
    #             DB_Manager().AddAdRequest(campaign, sid, userID, "INFL", "PENDING", msg, modified_budget, modified_terms, "False", "True")
    #         except Exception as exc:
    #             print(exc)
    #             flash("Failed to send message", "danger")

    #     inbox = DB_Manager().QueryInfluencerInBoxChat(userID, int(sid))
    #     camps = DB_Manager().QueryCampaignTitleID()
    #     camp_dict = {camps[0][i]: camps[1][i] for i in range(len(camps[0]))}
    #     return render_template("influencer/influencer_inbox_chat.html",
    #                            text="Influencer Inbox",
    #                            title="Influencer Inbox",
    #                            inbox=inbox,
    #                            camp_dict = camp_dict,
    #                            sponsor = User.query.filter_by(id=sid).first(),
    #                            btn_action="Influencer Inbox")
    
    # @app.route("/influencer/accept_ad_request/<iid>/<sid>/<status>", methods=["GET"], strict_slashes=False)
    # @e.influencer_required
    # def influencer_accept_ad_request(iid, sid, status):
    #     cid = request.args.get('cid')  # Accessing cid as a query parameter
    #     print(iid, sid, status, cid)
    #     if DB_Manager().updateAdRequestStatus(iid, sid, status, cid):
    #         flash("Ad request accepted successfully", "success")
    #     else:
    #         flash("Failed to accept ad request", "danger")
    #     return redirect(url_for('influencer_inbox_chat', sid=sid))
    
    # @app.route("/user/dashboard", methods=["GET"], strict_slashes=False)
    # @e.user_required
    # def user_dashboard():
    #     userID = current_user.get_id()
    #     return render_template("user/user_dash.html",
    #                            text="User Dashboard",
    #                            title="User Dashboard",
    #                            info = User.query.filter_by(id=userID).first(),
    #                            followers = DB_Manager().QueryFollowers(userID),
    #                            influencers = User.query.filter(User.user_type == "I").all(),
    #                            btn_action="User Dashboard")

    # @app.route("/user/update_dashboard", methods=["GET", "POST"], strict_slashes=False)
    # @e.user_required
    # def user_update_dashboard():
    #     userID = current_user.get_id()
    #     user = User.query.filter_by(id=userID).first()
    #     form = register_form_usr()
    #     if form.validate_on_submit():
    #         try:
    #             pwd = form.pwd.data
    #             username = form.username.data
    #             ph_no = form.ph_no.data

    #             user.pwd = bcrypt.generate_password_hash(pwd)
    #             user.username = username
    #             user.ph_no = ph_no

    #             db.session.commit()
    #             flash("Details updated", "success")
    #         except Exception as exc:
    #             db.session.rollback()
    #             flash("Failed to update details", "danger")
    #         return redirect(url_for('user_update_dashboard'))
    #     form.email.data = user.email
    #     form.username.data = user.username
    #     form.ph_no.data = user.ph_no
    #     return render_template("user/user_update_dashboard.html",
    #                              form=form,
    #                              text="User Update Dashboard",
    #                              title="User Update Dashboard",
    #                              btn_action="Update Dashboard")
    
    # @app.route("/user/search_influencer", methods=["GET"], strict_slashes=False)
    # @e.user_required
    # def user_search_influencer():
    #     userID = current_user.get_id()
    #     print(DB_Manager().QueryFollowers(userID))
    #     followers_to_ignore = set(DB_Manager().QueryFollowers(userID)[1])
    #     if len(followers_to_ignore) == 0:
    #         followers_to_ignore = [-1]
    #     # query all influencers which are not present in the followers_to_ignore list
    #     influencers = User.query.filter(User.user_type == "I", User.id.notin_(followers_to_ignore)).all()
    #     return render_template("user/user_search_influencer.html",
    #                            text="User Search Influencer",
    #                            title="User Search Influencer",
    #                            influencers=influencers,
    #                            btn_action="User Search Influencer")

    # @app.route("/user/follow/<iid>", methods=["GET"], strict_slashes=False)
    # @e.user_required
    # def user_follow(iid):
    #     userID = current_user.get_id()
    #     if DB_Manager().AddFollower(userID, iid):
    #         User.query.filter_by(id=iid).first().followers += 1
    #         db.session.commit()
    #         flash("Followed", "success")
    #     else:
    #         flash("Failed to follow", "danger")
    #     return redirect(url_for('user_dashboard'))

    # @app.route("/user/unfollow/<iid>", methods=["GET"], strict_slashes=False)
    # @e.user_required
    # def user_unfollow(iid):
    #     userID = current_user.get_id()
    #     if DB_Manager().RemoveFollower(userID, iid):
    #         User.query.filter_by(id=iid).first().followers -= 1
    #         db.session.commit()
    #         flash("Unfollowed", "success")
    #     else:
    #         flash("Failed to unfollow", "danger")
    #     return redirect(url_for('user_dashboard'))

    # @app.route("/delete_chat/<iid>/<sid>/<red>", methods=["GET"], strict_slashes=False)
    # @login_required
    # def delete_chat(iid, sid, red):
    #     if DB_Manager().RemoveChat(iid, sid):
    #         flash("Chat deleted", "success")
    #     else:
    #         flash("Failed to delete chat", "danger")
    #     if red == "S":
    #         return redirect(url_for('sponsor_inbox'))
    #     else:
    #         return redirect(url_for('influencer_inbox'))
    

app, socketio, dropzone = create_app()

server(app, socketio)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
