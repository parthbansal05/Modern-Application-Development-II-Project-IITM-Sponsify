import Vue from "vue";
import Router from "vue-router";

// Import your components here
import AdminDash from "@/components/admin/AdminDash.vue";
import AdminInsights from "@/components/admin/AdminInsights.vue";
import AdminViewAllCampaigns from "@/components/admin/AdminViewAllCampaigns.vue";
import AdminViewCampaign from "@/components/admin/AdminViewCampaign.vue";
import DeleteUser from "@/components/admin/DeleteUser.vue";

import InfluencerDash from "@/components/influencer/InfluencerDash.vue";
import InfluencerInbox from "@/components/influencer/InfluencerInbox.vue";
import InfluencerInboxChat from "@/components/influencer/InfluencerInboxChat.vue";
import InfluencerSearchCampaigns from "@/components/influencer/InfluencerSearchCampaigns.vue";
import InfluencerUpdateDashboard from "@/components/influencer/InfluencerUpdateDashboard.vue";

import CreateCampaign from "@/components/sponsor/CreateCampaign.vue";
import SponsorDash from "@/components/sponsor/SponsorDash.vue";
import SponsorInbox from "@/components/sponsor/SponsorInbox.vue";
import SponsorInboxChat from "@/components/sponsor/SponsorInboxChat.vue";
import SponsorSearchInfluencer from "@/components/sponsor/SponsorSearchInfluencer.vue";
import SponsorUpdateDashboard from "@/components/sponsor/SponsorUpdateDashboard.vue";
import SponsorViewCampaign from "@/components/sponsor/SponsorViewCampaign.vue";
import UpdateCampaign from "@/components/sponsor/UpdateCampaign.vue";

import UserDash from "@/components/user/UserDash.vue";
import UserSearchInfluencer from "@/components/user/UserSearchInfluencer.vue";
import UserUpdateDashboard from "@/components/user/UserUpdateDashboard.vue";


import LoginPage from "@/components/LoginPage.vue";
import LogoutPage from "@/components/LogoutPage.vue"; 
import RegisterInfluencer from "@/components/RegisterInfluencer.vue";
import RegisterSponsor from "@/components/RegisterSponsor.vue";
import RegisterUser from "@/components/RegisterUser.vue";


Vue.use(Router);

export default new Router({
  mode: "history", // Use HTML5 History mode
  routes: [
    {
      path: "/AdminDash",
      name: "AdminDash",
      component: AdminDash,
    },
    {
      path: "/AdminInsights",
      name: "AdminInsights",
      component: AdminInsights,
    },
    {
      path: "/AdminViewAllCampaigns",
      name: "AdminViewAllCampaigns",
      component: AdminViewAllCampaigns,
    },
    {
      path: "/AdminViewCampaign",
      name: "AdminViewCampaign",
      component: AdminViewCampaign,
    },
    {
      path: "/DeleteUser/:id", // Add a dynamic parameter :id
      name: "DeleteUser",
      component: DeleteUser,
    },
    {
      path: "/InfluencerDash",
      name: "InfluencerDash",
      component: InfluencerDash,
    },
    {
      path: "/InfluencerInbox",
      name: "InfluencerInbox",
      component: InfluencerInbox,
    },
    {
      path: "/InfluencerInboxChat",
      name: "InfluencerInboxChat",
      component: InfluencerInboxChat,
    },
    {
      path: "/InfluencerSearchCampaigns",
      name: "InfluencerSearchCampaigns",
      component: InfluencerSearchCampaigns,
    },
    {
      path: "/InfluencerUpdateDashboard",
      name: "InfluencerUpdateDashboard",
      component: InfluencerUpdateDashboard,
    },
    {
      path: "/CreateCampaign",
      name: "CreateCampaign",
      component: CreateCampaign,
    },
    {
      path: "/SponsorDash",
      name: "SponsorDash",
      component: SponsorDash,
    },
    {
      path: "/SponsorInbox",
      name: "SponsorInbox",
      component: SponsorInbox,
    },
    {
      path: "/SponsorInboxChat",
      name: "SponsorInboxChat",
      component: SponsorInboxChat,
    },
    {
      path: "/SponsorSearchInfluencer",
      name: "SponsorSearchInfluencer",
      component: SponsorSearchInfluencer,
    },
    {
      path: "/SponsorUpdateDashboard",
      name: "SponsorUpdateDashboard",
      component: SponsorUpdateDashboard,
    },
    {
      path: "/SponsorViewCampaign",
      name: "SponsorViewCampaign",
      component: SponsorViewCampaign,
    },
    {
      path: "/UpdateCampaign",
      name: "UpdateCampaign",
      component: UpdateCampaign,
    },
    {
      path: "/UserDash",
      name: "UserDash",
      component: UserDash,
    },
    {
      path: "/UserSearchInfluencer",
      name: "UserSearchInfluencer",
      component: UserSearchInfluencer,
    },
    {
      path: "/UserUpdateDashboard",
      name: "UserUpdateDashboard",
      component: UserUpdateDashboard,
    },
    {
      path: "/login",
      name: "LoginPage",
      component: LoginPage,
    },
    {
      path: '/logout',
      name: 'LogoutPage',
      component: LogoutPage
    },
    {
      path: "/registerInfluencer",
      name: "RegisterInfluencer",
      component: RegisterInfluencer,
    },
    {
      path: "/registerSponsor",
      name: "RegisterSponsor",
      component: RegisterSponsor,
    },
    {
      path: "/registerUser",
      name: "RegisterUser",
      component: RegisterUser,
    }
  ],
});
