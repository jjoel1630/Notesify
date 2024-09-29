// Chakra imports
import { useDisclosure, Stack, Box, useColorMode } from "@chakra-ui/react";
import {
	ArgonLogoDark,
	ArgonLogoLight,
	ChakraLogoDark,
	ChakraLogoLight,
} from "components/Icons/Icons";
// Layout components
import Sidebar from "components/Sidebar/Sidebar.js";
import React, { useState } from "react";
import { Redirect, Route, Switch } from "react-router-dom";
import routes from "routes.js";
// Custom components
import MainPanel from "../components/Layout/MainPanel";
import PanelContainer from "../components/Layout/PanelContainer";
import PanelContent from "../components/Layout/PanelContent";
import bgAdmin from "assets/img/admin-background.png";
import componentMap from "views/Dashboard/ComponentMap";
import { useHistory } from "react-router-dom";

export default function Dashboard(props) {
	const history = useHistory();

	const { ...rest } = props;
	// states and functions
	const [fixed, setFixed] = useState(false);
	const { colorMode } = useColorMode();
	// functions for changing the states from components
	const getRoute = () => {
		return window.location.pathname !== "/admin/full-screen-maps";
	};
	const getActiveRoute = (routes) => {
		let activeRoute = "Default Brand Text";
		for (let i = 0; i < routes.length; i++) {
			if (routes[i].collapse) {
				let collapseActiveRoute = getActiveRoute(routes[i].views);
				if (collapseActiveRoute !== activeRoute) {
					return collapseActiveRoute;
				}
			} else if (routes[i].category) {
				let categoryActiveRoute = getActiveRoute(routes[i].views);
				if (categoryActiveRoute !== activeRoute) {
					return categoryActiveRoute;
				}
			} else {
				if (window.location.href.indexOf(routes[i].layout + routes[i].path) !== -1) {
					return routes[i].name;
				}
			}
		}
		return activeRoute;
	};

	const getRoutes = (routes) => {
		// return routes.map((prop, key) => {
		// 	// console.log(prop.fileId);
		// 	// console.log(prop.audioId);
		// 	// console.log(prop.name);
		// 	// console.log(prop.layout + prop.path + key);
		// 	return (
		// 		<Route
		// 			path={prop.layout + prop.path}
		// 			component={(routeProps) => {
		// 				// Ensure no unnecessary re-renders happen
		// 				// console.log(prop);
		// 				return (
		// 					<prop.component
		// 						{...routeProps}
		// 						fileID={prop.fileId}
		// 						audioID={prop.audioId}
		// 						fileName={prop.name}
		// 						customProp="custom"
		// 					/>
		// 				);
		// 			}}
		// 			key={`${prop.layout}${prop.path}${prop.fileId}`}
		// 		/>
		// 	);
		// });
		// Retrieve uploaded files from local storage
		const storedFiles = JSON.parse(localStorage.getItem("uploadedFiles")) || [routes[0]];
		console.log(storedFiles);

		return storedFiles.map((fileData, key) => {
			// console.log(fileData);
			const RouteComponent = (routeProps) => {
				const ComponentToRender = componentMap["dashboard"];
				// console.log("FileData in RouteComponent:", fileData); // This should log correctly

				return (
					<ComponentToRender
						{...routeProps}
						fileID={fileData.fileId}
						audioID={fileData.audioId}
						fileName={fileData.name}
						customProp="custom"
					/>
				);
			};

			return (
				<Route
					path={`/${fileData.fileId}`} // Adjust this path as needed
					render={RouteComponent} // Use the new functional component
					key={`${fileData.fileId}${key}`} // Unique key for each route
				/>
			);
		});
	};
	const { isOpen, onOpen, onClose } = useDisclosure();
	document.documentElement.dir = "ltr";
	// Chakra Color Mode
	return (
		<Box>
			{/* <Box
				minH="40vh"
				w="100%"
				position="absolute"
				bgImage={colorMode === "light" ? bgAdmin : "none"}
				bg={colorMode === "light" ? bgAdmin : "navy.900"}
				bgSize="cover"
				top="0"
			/> */}
			<Sidebar
				routes={JSON.parse(localStorage.getItem("uploadedFiles")) || [routes[0]]}
				logo={
					<Stack direction="row" spacing="12px" align="center" justify="center">
						{colorMode === "dark" ? (
							<ArgonLogoLight w="74px" h="27px" />
						) : (
							<ArgonLogoDark w="74px" h="27px" />
						)}
						<Box w="1px" h="20px" bg={colorMode === "dark" ? "white" : "gray.700"} />
						{colorMode === "dark" ? (
							<ChakraLogoLight w="82px" h="21px" />
						) : (
							<ChakraLogoDark w="82px" h="21px" />
						)}
					</Stack>
				}
				display="none"
				{...rest}
			/>
			<MainPanel
				w={{
					base: "100%",
					xl: "calc(100% - 275px)",
				}}>
				<PanelContent>
					<PanelContainer>
						<Switch>
							{getRoutes(routes)}
							<Redirect from="/" to="audionote" />
						</Switch>
					</PanelContainer>
				</PanelContent>
			</MainPanel>
		</Box>
	);
}
