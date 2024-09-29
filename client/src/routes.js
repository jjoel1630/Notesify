// import
import React from "react";
import Dashboard from "views/Dashboard/Dashboard.js";
import Tables from "views/Dashboard/Tables.js";
import Billing from "views/Dashboard/Billing.js";

import { HomeIcon, StatsIcon, CreditIcon } from "components/Icons/Icons";

var dashRoutes = [
	{
		path: "audionote",
		name: "New Note",
		// icon: <HomeIcon color="inherit" />,
		component: Dashboard,
		layout: "/",
		fileId: "",
		audioId: "",
	},
	// {
	// 	path: "1",
	// 	name: "audio_file",
	// 	icon: <HomeIcon color="inherit" />,
	// 	component: Dashboard,
	// 	layout: "/",
	// 	fileId: "66f8601571da4941b14bafa9",
	// 	audioId: "66f84f23f2500e99053a5da3",
	// },
];
export default dashRoutes;
