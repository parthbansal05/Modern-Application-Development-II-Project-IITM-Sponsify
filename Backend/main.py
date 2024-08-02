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
from server_pkg.server.app import bcrypt, create_app, db, cache
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
                if user.user_type == "A":
                    redirect_url = "/AdminDash"
                elif user.user_type == "S":
                    if user.sponsor_approval == "False":
                        return jsonify({"error": "Sponsor account not approved yet"}), 200
                    redirect_url = "/SponsorDash"
                elif user.user_type == "I":
                    redirect_url = "/InfluencerDash"
                elif user.user_type == "U":
                    redirect_url = "/UserDash"
                
                access_token = create_access_token(identity=user.id, expires_delta = False)
                
                if next_url == "None" or next_url == None:
                    return jsonify(access_token=access_token, redirect_url = redirect_url)
                if not e.is_safe_url(next_url):
                    return jsonify({"error": "Bad URL"}), 400
                return jsonify(access_token=access_token, redirect_url = next_url)
            else:
                return jsonify({"error": "Wrong username or password"}), 401

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
                DB_Manager().AddModel(newuser.id, username, email, ph_no, user_type)
                return jsonify({"msg": "Account Successfully created"}), 200
            except IntegrityError as exc:
                db.session.rollback()
                print(exc)
                return jsonify({"error": "User already exists!"}), 200
            except Exception as exc:
                db.session.rollback()
                return jsonify({"error": "Something went wrong!"}), 200
    
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
                DB_Manager().AddModel(newuser.id, username, email, ph_no, user_type)
                return jsonify({"msg": "Account Successfully created"}), 200
            except IntegrityError as exc:
                db.session.rollback()
                return jsonify({"error": "User already exists!"}), 200
            except Exception as exc:
                db.session.rollback()
                return jsonify({"error": "Something went wrong!"}), 200

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
                DB_Manager().AddModel(newuser.id, username, email, ph_no, user_type)
                return jsonify({"msg": "Account Successfully created"}), 200
            except IntegrityError as exc:
                db.session.rollback()
                return jsonify({"error": "User already exists!"}), 200
            except Exception as exc:
                db.session.rollback()
                return jsonify({"error": "Something went wrong!"}), 200

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
            DB_Manager().DeleteModel(uid)
            return jsonify({"status": "Deleted"}), 200
        except Exception as exc:
            print(exc)
            return jsonify({"error": str(exc)}), 500

    # content page
    # admin pages
    @app.route("/admin/dashboard", methods=["GET"], strict_slashes=False)
    @e.admin_required
    @cache.cached(timeout=10, key_prefix=lambda: f"admin_dashboard_{get_jwt_id()}")
    def admin_dashboard():
        userID = get_jwt_id()
        campaigns = DB_Manager().QueryRecentCampaigns()
        
        influencer = ([[inf.id, inf.username, inf.email, inf.ph_no, inf.user_type, inf.category, inf.niche, inf.followers, inf.industry, inf.budget] for inf in User.query.filter(User.user_type == "I").all()])
        sponsors = ([[spo.id, spo.username, spo.email, spo.ph_no, spo.user_type, spo.category, spo.niche, spo.followers, spo.industry, spo.budget] for spo in User.query.filter(User.user_type == "S", User.sponsor_approval == "True").all()])
        users = ([[usr.id, usr.username, usr.email, usr.ph_no, usr.user_type, usr.category, usr.niche, usr.followers, usr.industry, usr.budget] for usr in User.query.filter(User.user_type == "U").all()])
        
        sponsor_approval_pending = ([[spo.id, spo.username, spo.email, spo.ph_no, spo.user_type, spo.category, spo.niche, spo.followers, spo.industry, spo.budget] for spo in User.query.filter(User.user_type == "S", User.sponsor_approval == "False").all()])
        print(sponsor_approval_pending, sponsors)
        camps = DB_Manager().QueryCampaignTitleID()
        camp_dict = {camps[0][i]: camps[1][i] for i in range(len(camps[0]))} if camps not in [None, []] else {}

        return jsonify(campaigns=campaigns,
                        users=users,
                        influencer=influencer,
                        sponsors=sponsors,
                        sponsor_approval_pending=sponsor_approval_pending,
                        camp_dict=camp_dict,
                        admin_email=str(User.query.filter_by(id=userID).first().email),
                        admin_phno=str(User.query.filter_by(id=userID).first().ph_no),
                        admin_username=str(User.query.filter_by(id=userID).first().username))

    @app.route("/admin/insights", methods=["GET"], strict_slashes=False)
    @e.admin_required
    @cache.cached(timeout=10, key_prefix=lambda: f"admin_insights_{get_jwt_id()}")
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
    @cache.cached(timeout=10, key_prefix=lambda: f"admin_view_campaign_{get_jwt_id()}")
    def admin_view_campaign(cid):
        cid = int(cid)
        campaign = DB_Manager().QueryCampaignByCID(cid)
        sponsors = ([[spo.id, spo.username, spo.email, spo.ph_no, spo.user_type, spo.category, spo.niche, spo.followers, spo.industry, spo.budget] for spo in User.query.filter(User.user_type == "S", User.sponsor_approval == "True").all()])
        return jsonify(campaign=campaign,
                       sponsors=sponsors)
    
    @app.route("/admin/view_all_campaigns", methods=["GET"], strict_slashes=False)
    @e.admin_required
    @cache.cached(timeout=10, key_prefix=lambda: f"admin_view_all_campaigns_{get_jwt_id()}")
    def admin_view_all_campaigns():
        campaigns=DB_Manager().QueryAllCampaigns()
        sponsors = ([[spo.id, spo.username, spo.email, spo.ph_no, spo.user_type, spo.category, spo.niche, spo.followers, spo.industry, spo.budget] for spo in User.query.filter(User.user_type == "S", User.sponsor_approval == "True").all()])        
        return jsonify(campaigns=campaigns,
                          sponsors=sponsors)
    
    @app.route("/admin/flag_campaign/<cid>", methods=["GET"], strict_slashes=False)
    @e.admin_required
    def admin_flag_campaign(cid):
        cid = int(cid)
        if DB_Manager().flagCampaign(cid):
            return jsonify({"msg": "Campaign flagged"}), 200
        else:
            return jsonify({"error": "Failed to flag campaign"}), 200
    
    @app.route("/admin/unflag_campaign/<cid>", methods=["GET"], strict_slashes=False)
    @e.admin_required
    def admin_unflag_campaign(cid):
        cid = int(cid)
        if DB_Manager().unflagCampaign(cid):
            return jsonify({"msg": "Campaign unflagged"}), 200
        else:
            return jsonify({"error": "Failed to unflag campaign"}), 200
        
    @app.route("/admin/approve_sponsor/<sid>", methods=["GET"], strict_slashes=False)
    @e.admin_required
    def admin_approve_sponsor(sid):
        sid = int(sid)
        if User.query.filter_by(id=sid).first().user_type != "S":
            return jsonify({"error": "Invalid sponsor id"}), 200
        User.query.filter_by(id=sid).first().sponsor_approval = "True"
        db.session.commit()
        return jsonify({"msg": "Sponsor approved"}), 200

    # # sponsor pages
    @app.route("/sponsor/dashboard", methods=["GET"], strict_slashes=False)
    @e.sponsor_required
    @cache.cached(timeout=10, key_prefix=lambda: f"sponsor_dashboard_{get_jwt_id()}")
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

    @app.route("/sponsor/view_campaigns/<cid>", methods=["GET"], strict_slashes=False)
    @e.sponsor_required
    @cache.cached(timeout=10, key_prefix=lambda: f"sponsor_view_campaigns_{get_jwt_id()}")
    def sponsor_view_campaigns(cid):
        cid = int(cid)
        campaign = DB_Manager().QueryCampaignByCID(cid)
        return jsonify(campaign=campaign)
    
    @app.route("/sponsor/create_campaign", methods=["POST"], strict_slashes=False)
    @e.sponsor_required
    def sponsor_create_campaign():
        if request.method == 'POST':
            data = request.json
            title = data.get('campTitle')
            description = data.get('campDesc')
            sdate = time.mktime(time.strptime(str(data.get('startDate')), "%Y-%m-%d"))
            edate = time.mktime(time.strptime(str(data.get('endDate')), "%Y-%m-%d"))
            budget = data.get('budget')
            visibility = data.get('visibility')
            goal = data.get('goal')
            flagged = "NO"
            SID = get_jwt_id()
            print(SID)
            
            print(data)
            try:
                if DB_Manager().AddCampaigns(SID, title, description, sdate, edate, budget, visibility, goal, flagged):
                    return jsonify({"msg": "Campaign created"}), 200
                else:
                    return jsonify({"error": "Failed to create campaign"}), 500
            except Exception as exc:
                print(exc)
                return jsonify({"error": "Failed to create campaign"}), 500

    @app.route("/sponsor/update_campaign/<cid>", methods=["GET", "POST"], strict_slashes=False)
    @e.sponsor_required
    def sponsor_update_campaign(cid):
        cid = int(cid)
        campaign = DB_Manager().QueryCampaignByCID(cid)
        if request.method == 'POST':
            data = request.json
            title = data.get('campTitle')
            description = data.get('campDesc')
            sdate = time.mktime(time.strptime(str(data.get('startDate')), "%Y-%m-%d"))
            edate = time.mktime(time.strptime(str(data.get('endDate')), "%Y-%m-%d"))
            budget = data.get('budget')
            visibility = data.get('visibility')
            goal = data.get('goal')
            print(data)
            try:
                if DB_Manager().UpdateCampaigns(cid, title, description, sdate, edate, budget, visibility, goal):
                    return jsonify({"msg": "Campaign updated"}), 200
                else:
                    return jsonify({"error": "Failed to update campaign"}), 500
            except Exception as exc:
                print(exc)
                return jsonify({"error": "Failed to update campaign"}), 500
        
        elif request.method == 'GET':
            print(campaign)
            return jsonify(campTitle=campaign[2][0],
                           campDesc=campaign[3][0],
                           startDate=campaign[4][0],
                           endDate=campaign[5][0],
                           budget=campaign[6][0],
                           visibility=campaign[7][0],
                           goal=campaign[8][0])
    
    @app.route("/sponsor/delete_campaign/<cid>", methods=["GET"], strict_slashes=False)
    @e.sponsor_required
    def sponsor_delete_campaign(cid):
        cid = int(cid)
        if DB_Manager().RemoveCampaign(cid):
            return jsonify({"msg": "Campaign deleted"}), 200
        else:
            return jsonify({"error": "Failed to delete campaign"}), 500
        return redirect(url_for('sponsor_dashboard'))

    @app.route("/sponsor/inbox", methods=["GET"], strict_slashes=False)
    @e.sponsor_required
    @cache.cached(timeout=10, key_prefix=lambda: f"sponsor_inbox_{get_jwt_id()}")
    def sponsor_inbox():
        userID = get_jwt_id()
        inbox = DB_Manager().QuerySponsorInBoxChatOverView(userID)
        camps = DB_Manager().QueryCampaignTitleID()
        camp_dict = {camps[0][i]: camps[1][i] for i in range(len(camps[0]))}
        influencer = ([[inf.id, inf.username, inf.email, inf.ph_no, inf.user_type, inf.category, inf.niche, inf.followers, inf.industry, inf.budget] for inf in User.query.filter(User.user_type == "I").all()])
        return jsonify(inbox=inbox,
                          camp_dict=camp_dict,
                          influencer=influencer)
    
    @app.route("/sponsor/inbox/<iid>", methods=["GET", "POST"], strict_slashes=False)
    @e.sponsor_required
    @cache.cached(timeout=5, key_prefix=lambda: f"sponsor_inbox_chat_{get_jwt_id()}")
    def sponsor_inbox_chat(iid):
        userID = get_jwt_id()
        DB_Manager().updateAdRequestSeenSOPN(iid, userID)
        if request.method == 'POST':
            data = request.json
            msg = data.get('message')
            campaign = data.get('campaign')
            modified_budget = data.get('modified_budget')
            modified_terms = data.get('modified_terms')
            print(data)

            try:
                if msg == "" and modified_budget == "" and modified_terms == "": raise Exception("Empty message")
                if modified_budget == "": modified_budget = DB_Manager().QuerySponsorInBoxChatLastBudget(int(iid), userID, campaign)[0][0]
                if modified_terms == "": modified_terms = DB_Manager().QuerySponsorInBoxChatLastTerm(int(iid), userID, campaign)[0][0]
                DB_Manager().AddAdRequest(campaign, userID, iid, "SOPN", "PENDING", msg, modified_budget, modified_terms, "True", "False")
            except Exception as exc:
                print(exc)
                return jsonify({"error": "Failed to send message"}), 500
        if request.method == 'GET':            
            inbox = DB_Manager().QuerySponsorInBoxChat(userID, int(iid))
            camps = DB_Manager().QueryCampaignTitleID()
            camp_dict = {camps[0][i]: camps[1][i] for i in range(len(camps[0]))}
            inf = User.query.filter_by(id=iid).first()
            influencer = ([inf.id, inf.username, inf.email, inf.ph_no, inf.user_type, inf.category, inf.niche, inf.followers, inf.industry, inf.budget])
            return jsonify(inbox=inbox,
                            camp_dict=camp_dict,
                            influencer=influencer)
    
    @app.route("/sponsor/accept_ad_request/<iid>/<sid>/<cid>/<status>", methods=["GET"], strict_slashes=False)
    @e.sponsor_required
    def sponsor_accept_ad_request(iid, sid, cid, status):
        print(iid, sid, status, cid)
        if DB_Manager().updateAdRequestStatus(iid, sid, status, cid):
            return jsonify({"msg": "Ad request accepted"}), 200
        else:
            return jsonify({"error": "Failed to accept ad request"}), 500
    
    @app.route("/sponsor/search_influencer", methods=["GET"], strict_slashes=False)
    @e.sponsor_required
    @cache.cached(timeout=5, key_prefix=lambda: f"sponsor_search_influencer_{get_jwt_id()}")
    def sponsor_search_influencer():
        userID = get_jwt_id()
        influencers = ([[inf.id, inf.username, inf.email, inf.ph_no, inf.user_type, inf.category, inf.niche, inf.followers, inf.industry, inf.budget] for inf in User.query.filter_by(user_type="I").all()])
        campaigns = DB_Manager().QueryCampaignIDAndNameAndBudgetBySID(userID)
        unique_niches = list(set([inf[6] for inf in influencers]))
        unique_categories = list(set([inf[5] for inf in influencers]))
        return jsonify(influencers=influencers,
                        campaigns=campaigns,
                        unique_niches=unique_niches,
                        unique_categories=unique_categories)
    
    @app.route("/sponsor/initiate_chat/<cid>/<iid>/<budget>", methods=["GET"], strict_slashes=False)
    @e.sponsor_required
    def sponsor_initiate_chat(cid, iid, budget):
        userID = get_jwt_id()
        msg = "Hi, would you like to collaborate on my campaign?"
        if DB_Manager().AddAdRequest(cid, userID, iid, "SOPN", "PENDING", msg, budget, "", "True", "False"):
            return jsonify({"msg": "Chat initiated successfully"}), 200
        else:
            return jsonify({"error": "Failed to initiate chat"}), 500
    
    @app.route("/influencer/dashboard", methods=["GET"], strict_slashes=False)
    @e.influencer_required
    @cache.cached(timeout=10, key_prefix=lambda: f"influencer_dashboard_{get_jwt_id()}")
    def influencer_dashboard():
        userID = get_jwt_id()
        inf = User.query.filter_by(id=userID).first()
        influencer = ([inf.id, inf.username, inf.email, inf.ph_no, inf.user_type, inf.category, inf.niche, inf.followers, inf.industry, inf.budget])
        return jsonify(info=influencer)

    @app.route("/influencer/dashboard/<iid>", methods=["GET"], strict_slashes=False)
    @jwt_required()
    @cache.cached(timeout=10, key_prefix=lambda: f"influencer_dashboard_iid_{get_jwt_id()}")
    def influencer_dashboard_iid(iid):
        inf = User.query.filter_by(id=iid).first()
        if inf.user_type != "I":
            return jsonify({"error": "Invalid influencer id"}), 400
        influencer = ([inf.id, inf.username, inf.email, inf.ph_no, inf.user_type, inf.category, inf.niche, inf.followers, inf.industry, inf.budget])
        return jsonify(info=influencer)
    
    @app.route("/influencer/update_dashboard", methods=["GET", "POST"], strict_slashes=False)
    @e.influencer_required
    def influencer_update_dashboard():
        userID = get_jwt_id()
        user = User.query.filter_by(id=userID).first()
        if request.method == 'POST':
            data = request.json
            username = data.get('username')
            pwd = data.get('pwd')
            ph_no = data.get('ph_no')
            category = data.get('category')
            niche = data.get('niche')
            try:
                user.pwd = bcrypt.generate_password_hash(pwd)
                user.username = username
                user.ph_no = ph_no
                user.category = category
                user.niche = niche

                db.session.commit()
                return jsonify({"msg": "Details updated"}), 200
            except Exception as exc:
                db.session.rollback()
                print(exc)
                return jsonify({"error": "Failed to update details"}), 500
        elif request.method == 'GET':
            return jsonify(email=user.email,
                           username=user.username,
                           ph_no=user.ph_no,
                           category=user.category,
                           niche=user.niche)

    @app.route("/influencer/search_campaigns", methods=["GET"], strict_slashes=False)
    @e.influencer_required
    @cache.cached(timeout=5, key_prefix=lambda: f"influencer_search_campaigns_{get_jwt_id()}")
    def influencer_search_campaigns():
        campaigns = DB_Manager().QueryPublicCampaign()
        print(campaigns)
        unique_start_times = list(set(campaigns[4])) if campaigns != [] else []
        unique_budgets = list(set(campaigns[6])) if campaigns != [] else []
        return jsonify(campaigns=campaigns,
                        unique_start_times=unique_start_times,
                        unique_budgets=unique_budgets)
    
    @app.route("/influencer/initiate_chat/<cid>/<sid>/<budget>", methods=["GET"], strict_slashes=False)
    @e.influencer_required
    def influencer_initiate_chat(cid, sid, budget):
        userID = get_jwt_id()
        msg = "Hi, I am interested in your campaign. Can we discuss more about it?"
        if DB_Manager().AddAdRequest(cid, sid, userID, "INFL", "PENDING", msg, budget, "", "False", "True"):
            return jsonify({"msg": "Chat initiated successfully"}), 200
        else:
            return jsonify({"error": "Failed to initiate chat"}), 500
    
    @app.route("/influencer/inbox", methods=["GET"], strict_slashes=False)
    @e.influencer_required
    @cache.cached(timeout=10, key_prefix=lambda: f"influencer_inbox_{get_jwt_id()}")
    def influencer_inbox():
        userID = get_jwt_id()
        inbox = DB_Manager().QueryInfluencerInBoxChatOverView(userID)
        camps = DB_Manager().QueryCampaignTitleID()
        camp_dict = {camps[0][i]: camps[1][i] for i in range(len(camps[0]))} if camps not in [None, []] else {}
        sponsors = ([[spo.id, spo.username, spo.email, spo.ph_no, spo.user_type, spo.category, spo.niche, spo.followers, spo.industry, spo.budget] for spo in User.query.filter(User.user_type == "S", User.sponsor_approval == "True").all()])
        return jsonify(inbox=inbox,
                          camp_dict=camp_dict,
                          sponsors=sponsors)
    
    @app.route("/influencer/inbox/<sid>", methods=["GET", "POST"], strict_slashes=False)
    @e.influencer_required
    @cache.cached(timeout=5, key_prefix=lambda: f"influencer_inbox_chat_{get_jwt_id()}")
    def influencer_inbox_chat(sid):
        userID = get_jwt_id()
        if User.query.filter_by(id=sid).first().sponsor_approval == "False":
            return jsonify({"error": "Sponsor account not approved yet"}), 200
        DB_Manager().updateAdRequestSeenINFL(userID, sid)
        if request.method == "POST":
            data = request.json
            msg = data.get('message')
            campaign = data.get('campaign')
            modified_budget = data.get('modified_budget')
            modified_terms = data.get('modified_terms')
            print(data)
            try:                
                if msg == "" and modified_budget == "" and modified_terms == "": raise Exception("Empty message")
                if modified_budget == "": modified_budget = DB_Manager().QueryInfluencerInBoxChatLastBudget(userID, int(sid), campaign)[0][0]
                if modified_terms == "": modified_terms = DB_Manager().QueryInfluencerInBoxChatLastTerm(userID, int(sid), campaign)[0][0]
                DB_Manager().AddAdRequest(campaign, sid, userID, "INFL", "PENDING", msg, modified_budget, modified_terms, "False", "True")
            except Exception as exc:
                print(exc)
                return jsonify({"error": "Failed to send message"}), 500
            return "ok"
        if request.method == "GET":
            inbox = DB_Manager().QueryInfluencerInBoxChat(userID, int(sid))
            camps = DB_Manager().QueryCampaignTitleID()
            camp_dict = {camps[0][i]: camps[1][i] for i in range(len(camps[0]))}
            spo = User.query.filter_by(id=sid).first()
            sponsor = ([spo.id, spo.username, spo.email, spo.ph_no, spo.user_type, spo.category, spo.niche, spo.followers, spo.industry, spo.budget])
            return jsonify(inbox=inbox,
                            camp_dict=camp_dict,
                            sponsor=sponsor)
    
    @app.route("/influencer/accept_ad_request/<iid>/<sid>/<cid>/<status>", methods=["GET"], strict_slashes=False)
    @e.influencer_required
    def influencer_accept_ad_request(iid, sid, cid, status):
        print(iid, sid, status, cid)
        if DB_Manager().updateAdRequestStatus(iid, sid, status, cid):
            return jsonify({"msg": "Ad request accepted"}), 200
        else:
            return jsonify({"error": "Failed to accept ad request"}), 500
    
    @app.route("/user/dashboard", methods=["GET"], strict_slashes=False)
    @e.user_required
    @cache.cached(timeout=10, key_prefix=lambda: f"user_dashboard_{get_jwt_id()}")
    def user_dashboard():
        userID = get_jwt_id()
        usr = User.query.filter_by(id=userID).first()
        info = ([usr.id, usr.username, usr.email, usr.ph_no, usr.user_type, usr.category, usr.niche, usr.followers, usr.industry, usr.budget])
        influencer = ([[inf.id, inf.username, inf.email, inf.ph_no, inf.user_type, inf.category, inf.niche, inf.followers, inf.industry, inf.budget] for inf in User.query.filter(User.user_type == "I").all()])
        followers = DB_Manager().QueryFollowers(userID)
        return jsonify(info=info,
                          followers=followers,
                          influencers=influencer)

    @app.route("/user/update_dashboard", methods=["GET", "POST"], strict_slashes=False)
    @e.user_required
    def user_update_dashboard():
        userID = get_jwt_id()
        user = User.query.filter_by(id=userID).first()
        if request.method == 'POST':
            data = request.json
            username = data.get('username')
            pwd = data.get('pwd')
            ph_no = data.get('ph_no')
            try:
                user.pwd = bcrypt.generate_password_hash(pwd)
                user.username = username
                user.ph_no = ph_no

                db.session.commit()
                return jsonify({"msg": "Details updated"}), 200
            except Exception as exc:
                db.session.rollback()
                return jsonify({"error": "Failed to update details"}), 500
        elif request.method == 'GET':
            return jsonify(email=user.email,
                           username=user.username,
                           ph_no=user.ph_no)
    
    @app.route("/user/search_influencer", methods=["GET"], strict_slashes=False)
    @e.user_required
    @cache.cached(timeout=10, key_prefix=lambda: f"user_search_influencer_{get_jwt_id()}")
    def user_search_influencer():
        userID = get_jwt_id()
        print(DB_Manager().QueryFollowers(userID))
        followers_to_ignore = set(DB_Manager().QueryFollowers(userID)[1])
        if len(followers_to_ignore) == 0:
            followers_to_ignore = [-1]
        influencers = ([[inf.id, inf.username, inf.email, inf.ph_no, inf.user_type, inf.category, inf.niche, inf.followers, inf.industry, inf.budget] for inf in User.query.filter(User.user_type == "I", User.id.notin_(followers_to_ignore)).all()])
        unique_niches = list(set([inf[6] for inf in influencers]))
        unique_categories = list(set([inf[5] for inf in influencers]))
        return jsonify(influencers=influencers,
                        unique_niches=unique_niches,
                        unique_categories=unique_categories)

    @app.route("/user/follow/<iid>", methods=["GET"], strict_slashes=False)
    @e.user_required
    def user_follow(iid):
        userID = get_jwt_id()
        if DB_Manager().AddFollower(userID, iid):
            User.query.filter_by(id=iid).first().followers += 1
            db.session.commit()
            return jsonify({"msg": "Followed"}), 200
        else:
            return jsonify({"error": "Failed to follow"}), 500

    @app.route("/user/unfollow/<iid>", methods=["GET"], strict_slashes=False)
    @e.user_required
    def user_unfollow(iid):
        userID = get_jwt_id()
        print(iid, userID)
        if DB_Manager().RemoveFollower(userID, iid):
            User.query.filter_by(id=iid).first().followers -= 1
            db.session.commit()
            return jsonify({"msg": "Unfollowed"}), 200
        else:
            return jsonify({"error": "Failed to unfollow"}), 500

    @app.route("/delete_chat/<iid>/<sid>/<red>", methods=["GET"], strict_slashes=False)
    @jwt_required
    def delete_chat(iid, sid, red):
        if DB_Manager().RemoveChat(iid, sid):
            return jsonify({"msg": "Chat deleted"}), 200
        else:
            return jsonify({"error": "Failed to delete chat"}), 500
        
    @app.route("/get_username", methods=["GET"], strict_slashes=False)
    @cache.cached(timeout=10, key_prefix=lambda: f"get_username_{get_jwt_id()}")
    def get_username():
        userID = get_jwt_id()
        utype_mapper = {'S': 'Sponsor', 'I': 'Influencer', 'A': 'Admin', 'U': 'User'}
        return jsonify(username=User.query.filter_by(id=userID).first().username,
                          user_type=utype_mapper[User.query.filter_by(id=userID).first().user_type]), 200
    

app, socketio, dropzone = create_app()

server(app, socketio)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
