/*eslint-disable*/
import { EditIcon, HamburgerIcon } from "@chakra-ui/icons";
// chakra imports
import {
	Box,
	Button,
	Drawer,
	DrawerBody,
	DrawerCloseButton,
	DrawerContent,
	DrawerOverlay,
	Flex,
	Image,
	Stack,
	Text,
	useColorMode,
	useColorModeValue,
	useDisclosure,
} from "@chakra-ui/react";
import IconBox from "components/Icons/IconBox";
import { HomeIcon } from "components/Icons/Icons";
import {
	renderThumbDark,
	renderThumbLight,
	renderTrack,
	renderTrackRTL,
	renderView,
	renderViewRTL,
} from "components/Scrollbar/Scrollbar";
import { HSeparator } from "components/Separator/Separator";
import React from "react";
import { Scrollbars } from "react-custom-scrollbars";
import { NavLink, useLocation } from "react-router-dom";
import logoImg from "../../assets/img/logoimg.png";

// FUNCTIONS

function Sidebar(props) {
	// to check for active links and opened collapses
	let location = useLocation();
	// this is for the rest of the collapses
	const [state, setState] = React.useState({});
	const mainPanel = React.useRef();
	let variantChange = "0.2s linear";
	// verifies if routeName is the one active (in browser input)
	const activeRoute = (routeName) => {
		return location.pathname === routeName ? "active" : "";
	};
	const { colorMode } = useColorMode;
	// this function creates the links and collapses that appear in the sidebar (left menu)
	const { sidebarVariant } = props;
	const createLinks = (routes) => {
		// Chakra Color Mode
		// let activeBg = useColorModeValue("white", "navy.700");
		// let inactiveBg = useColorModeValue("white", "navy.700");
		// let activeColor = useColorModeValue("gray.700", "white");
		// let inactiveColor = useColorModeValue("gray.400", "gray.400");
		// let sidebarActiveShadow = "0px 7px 11px rgba(0, 0, 0, 0.04)";
		let activeBg = useColorModeValue("navy.700", "navy.700"); // Active background color for dark mode
		let inactiveBg = useColorModeValue("navy.800", "navy.800"); // Slightly different inactive background for dark mode
		let activeColor = useColorModeValue("white", "white"); // Active text color for dark mode
		let inactiveColor = useColorModeValue("gray.400", "gray.400"); // Inactive text color remains the same
		let sidebarActiveShadow = "0px 7px 11px rgba(0, 0, 0, 0.04)";

		return routes.map((prop, key) => {
			// if (prop.redirect) {
			// 	return null;
			// }
			// if (prop.category) {
			// 	var st = {};
			// 	st[prop["state"]] = !state[prop.state];
			// 	return (
			// 		<>
			// 			<Text
			// 				color={activeColor}
			// 				fontWeight="bold"
			// 				mb={{
			// 					xl: "6px",
			// 				}}
			// 				mx="auto"
			// 				ps={{
			// 					sm: "10px",
			// 					xl: "16px",
			// 				}}
			// 				py="12px">
			// 				{prop.name}
			// 			</Text>
			// 			{createLinks(prop.views)}
			// 		</>
			// 	);
			// }
			return (
				<NavLink to={prop.layout + prop.path} key={key}>
					{activeRoute(prop.layout + prop.path) === "active" ? (
						<>
							<Button
								boxSize="initial"
								justifyContent="flex-start"
								alignItems="center"
								boxShadow={sidebarActiveShadow}
								bg="gray.600"
								transition={variantChange}
								// mb={{
								// 	xl: "6px",
								// }}
								// mx={{
								// 	xl: "auto",
								// }}
								// ps={{
								// 	sm: "10px",
								// 	xl: "16px",
								// }}
								py="12px"
								borderRadius="15px"
								_hover="none"
								w="295px"
								ml="5px"
								mt="5px"
								mb="7px"
								_active={{
									bg: "inherit",
									transform: "none",
									borderColor: "transparent",
								}}
								_focus={{
									boxShadow: "0px 7px 11px rgba(0, 0, 0, 0.04)",
								}}>
								<Flex>
									{typeof prop.icon === "string" ? (
										<Icon>{prop.icon}</Icon>
									) : (
										<IconBox
											// bg="blue.500"
											color="white"
											h="30px"
											w="30px"
											me="12px"
											transition={variantChange}>
											<EditIcon color="inherit" />
										</IconBox>
									)}
									<Text color="white" my="auto" fontSize="sm">
										{document.documentElement.dir === "rtl"
											? prop.rtlName
											: prop.name}
									</Text>
								</Flex>
							</Button>
							{/* <Button
								boxSize="initial"
								justifyContent="flex-start"
								alignItems="center"
								boxShadow={sidebarActiveShadow}
								bg="gray.700"
								transition={variantChange}
								// mb={{
								// 	xl: "6px",
								// }}
								// mx={{
								// 	xl: "auto",
								// }}
								// ps={{
								// 	sm: "10px",
								// 	xl: "16px",
								// }}
								py="12px"
								borderRadius="15px"
								_hover="none"
								w="295px"
								ml="5px"
								mt="5px"
								mb="7px"
								_active={{
									bg: "inherit",
									transform: "none",
									borderColor: "transparent",
								}}
								_focus={{
									boxShadow: "0px 7px 11px rgba(0, 0, 0, 0.04)",
								}}>
								<Flex>
									{typeof prop.icon === "string" ? (
										<Icon>{prop.icon}</Icon>
									) : (
										<IconBox
											// bg="blue.500"
											color="white"
											h="30px"
											w="30px"
											me="12px"
											transition={variantChange}>
											<EditIcon color="inherit" />
										</IconBox>
									)}
									<Text color="white" my="auto" fontSize="sm">
										2050 ladha midterm 1 notes
									</Text>
								</Flex>
							</Button>
							<Button
								boxSize="initial"
								justifyContent="flex-start"
								alignItems="center"
								boxShadow={sidebarActiveShadow}
								bg="gray.700"
								transition={variantChange}
								// mb={{
								// 	xl: "6px",
								// }}
								// mx={{
								// 	xl: "auto",
								// }}
								// ps={{
								// 	sm: "10px",
								// 	xl: "16px",
								// }}
								py="12px"
								borderRadius="15px"
								_hover="none"
								w="295px"
								ml="5px"
								mt="5px"
								mb="7px"
								_active={{
									bg: "inherit",
									transform: "none",
									borderColor: "transparent",
								}}
								_focus={{
									boxShadow: "0px 7px 11px rgba(0, 0, 0, 0.04)",
								}}>
								<Flex>
									{typeof prop.icon === "string" ? (
										<Icon>{prop.icon}</Icon>
									) : (
										<IconBox
											// bg="blue.500"
											color="white"
											h="30px"
											w="30px"
											me="12px"
											transition={variantChange}>
											<EditIcon color="inherit" />
										</IconBox>
									)}
									<Text color="white" my="auto" fontSize="sm">
										1554 barone midterm 2
									</Text>
								</Flex>
							</Button>
							<Button
								boxSize="initial"
								justifyContent="flex-start"
								alignItems="center"
								boxShadow={sidebarActiveShadow}
								bg="gray.700"
								transition={variantChange}
								// mb={{
								// 	xl: "6px",
								// }}
								// mx={{
								// 	xl: "auto",
								// }}
								// ps={{
								// 	sm: "10px",
								// 	xl: "16px",
								// }}
								py="12px"
								borderRadius="15px"
								_hover="none"
								w="295px"
								ml="5px"
								mt="5px"
								mb="7px"
								_active={{
									bg: "inherit",
									transform: "none",
									borderColor: "transparent",
								}}
								_focus={{
									boxShadow: "0px 7px 11px rgba(0, 0, 0, 0.04)",
								}}>
								<Flex>
									{typeof prop.icon === "string" ? (
										<Icon>{prop.icon}</Icon>
									) : (
										<IconBox
											// bg="blue.500"
											color="white"
											h="30px"
											w="30px"
											me="12px"
											transition={variantChange}>
											<EditIcon color="inherit" />
										</IconBox>
									)}
									<Text color="white" my="auto" fontSize="sm">
										habitable planet
									</Text>
								</Flex>
							</Button>
							<Button
								boxSize="initial"
								justifyContent="flex-start"
								alignItems="center"
								boxShadow={sidebarActiveShadow}
								bg="gray.700"
								transition={variantChange}
								// mb={{
								// 	xl: "6px",
								// }}
								// mx={{
								// 	xl: "auto",
								// }}
								// ps={{
								// 	sm: "10px",
								// 	xl: "16px",
								// }}
								py="12px"
								borderRadius="15px"
								_hover="none"
								w="295px"
								ml="5px"
								mt="5px"
								mb="7px"
								_active={{
									bg: "inherit",
									transform: "none",
									borderColor: "transparent",
								}}
								_focus={{
									boxShadow: "0px 7px 11px rgba(0, 0, 0, 0.04)",
								}}>
								<Flex>
									{typeof prop.icon === "string" ? (
										<Icon>{prop.icon}</Icon>
									) : (
										<IconBox
											// bg="blue.500"
											color="white"
											h="30px"
											w="30px"
											me="12px"
											transition={variantChange}>
											<EditIcon color="inherit" />
										</IconBox>
									)}
									<Text color="white" my="auto" fontSize="sm">
										apph wellness notes
									</Text>
								</Flex>
							</Button>
							<Button
								boxSize="initial"
								justifyContent="flex-start"
								alignItems="center"
								boxShadow={sidebarActiveShadow}
								bg="gray.700"
								transition={variantChange}
								// mb={{
								// 	xl: "6px",
								// }}
								// mx={{
								// 	xl: "auto",
								// }}
								// ps={{
								// 	sm: "10px",
								// 	xl: "16px",
								// }}
								py="12px"
								borderRadius="15px"
								_hover="none"
								w="295px"
								ml="5px"
								mt="5px"
								mb="7px"
								_active={{
									bg: "inherit",
									transform: "none",
									borderColor: "transparent",
								}}
								_focus={{
									boxShadow: "0px 7px 11px rgba(0, 0, 0, 0.04)",
								}}>
								<Flex>
									{typeof prop.icon === "string" ? (
										<Icon>{prop.icon}</Icon>
									) : (
										<IconBox
											// bg="blue.500"
											color="white"
											h="30px"
											w="30px"
											me="12px"
											transition={variantChange}>
											<EditIcon color="inherit" />
										</IconBox>
									)}
									<Text color="white" my="auto" fontSize="sm">
										bio 1108 summary
									</Text>
								</Flex>
							</Button>
							<Button
								boxSize="initial"
								justifyContent="flex-start"
								alignItems="center"
								boxShadow={sidebarActiveShadow}
								bg="gray.700"
								transition={variantChange}
								// mb={{
								// 	xl: "6px",
								// }}
								// mx={{
								// 	xl: "auto",
								// }}
								// ps={{
								// 	sm: "10px",
								// 	xl: "16px",
								// }}
								py="12px"
								borderRadius="15px"
								_hover="none"
								w="295px"
								ml="5px"
								mt="5px"
								mb="7px"
								_active={{
									bg: "inherit",
									transform: "none",
									borderColor: "transparent",
								}}
								_focus={{
									boxShadow: "0px 7px 11px rgba(0, 0, 0, 0.04)",
								}}>
								<Flex>
									{typeof prop.icon === "string" ? (
										<Icon>{prop.icon}</Icon>
									) : (
										<IconBox
											// bg="blue.500"
											color="white"
											h="30px"
											w="30px"
											me="12px"
											transition={variantChange}>
											<EditIcon color="inherit" />
										</IconBox>
									)}
									<Text color="white" my="auto" fontSize="sm">
										psych 1101 prof thomas
									</Text>
								</Flex>
							</Button>
							<Button
								boxSize="initial"
								justifyContent="flex-start"
								alignItems="center"
								boxShadow={sidebarActiveShadow}
								bg="gray.700"
								transition={variantChange}
								// mb={{
								// 	xl: "6px",
								// }}
								// mx={{
								// 	xl: "auto",
								// }}
								// ps={{
								// 	sm: "10px",
								// 	xl: "16px",
								// }}
								py="12px"
								borderRadius="15px"
								_hover="none"
								w="295px"
								ml="5px"
								mt="5px"
								mb="7px"
								_active={{
									bg: "inherit",
									transform: "none",
									borderColor: "transparent",
								}}
								_focus={{
									boxShadow: "0px 7px 11px rgba(0, 0, 0, 0.04)",
								}}>
								<Flex>
									{typeof prop.icon === "string" ? (
										<Icon>{prop.icon}</Icon>
									) : (
										<IconBox
											// bg="blue.500"
											color="white"
											h="30px"
											w="30px"
											me="12px"
											transition={variantChange}>
											<EditIcon color="inherit" />
										</IconBox>
									)}
									<Text color="white" my="auto" fontSize="sm">
										chem 1212k lab prep
									</Text>
								</Flex>
							</Button> */}
						</>
					) : (
						<Button
							boxSize="initial"
							justifyContent="flex-start"
							alignItems="center"
							bg="transparent"
							mb={{
								xl: "6px",
							}}
							mx={{
								xl: "auto",
							}}
							py="12px"
							ps={{
								sm: "10px",
								xl: "16px",
							}}
							borderRadius="15px"
							_hover="none"
							w="100%"
							_active={{
								bg: "inherit",
								transform: "none",
								borderColor: "transparent",
							}}
							_focus={{
								boxShadow: "none",
							}}>
							<Flex>
								{typeof prop.icon === "string" ? (
									<Icon>{prop.icon}</Icon>
								) : (
									<IconBox
										// bg={inactiveBg}
										// color="blue.500"
										h="30px"
										w="30px"
										me="12px"
										transition={variantChange}>
										<HomeIcon color="inherit" />
									</IconBox>
								)}
								<Text color={inactiveColor} my="auto" fontSize="sm">
									{document.documentElement.dir === "rtl"
										? prop.rtlName
										: prop.name}
								</Text>
							</Flex>
						</Button>
					)}
				</NavLink>
			);
		});
	};
	const { logo, routes } = props;

	var links = <>{createLinks(routes)}</>;
	//  BRAND
	//  Chakra Color Mode
	const sidebarBg = useColorModeValue("white", "gray.800");
	let sidebarRadius = "20px";
	let sidebarMargins = "0px";
	var brand = (
		<Box pt={"25px"} mb="12px">
			{logo}
			<HSeparator my="26px" />
		</Box>
	);

	// SIDEBAR
	return (
		<Box ref={mainPanel}>
			<Box
				bg="gray.800"
				display={{ sm: "none", xl: "block" }}
				position="fixed"
				// top="120"
				// left="120"
				zIndex="1000">
				<Box
					transition={variantChange}
					w="320px"
					// maxW="280px"
					// ms={{
					// 	sm: "16px",
					// }}
					// my={{
					// 	sm: "16px",
					// }}
					h="calc(100vh)"
					bg="gray.700"
					ps="7px"
					pe="7px"
					// m={sidebarMargins}
					// filter="drop-shadow(0px 5px 14px rgba(0, 0, 0, 0.05))"
					// borderRadius={sidebarRadius}
				>
					<Scrollbars
						autoHide
						renderTrackVertical={
							document.documentElement.dir === "rtl" ? renderTrackRTL : renderTrack
						}
						renderThumbVertical={useColorModeValue(renderThumbLight, renderThumbDark)}
						renderView={
							document.documentElement.dir === "rtl" ? renderViewRTL : renderView
						}>
						<Box h="10px" />
						<Stack direction="column" mb="40px">
							<Box>{links}</Box>
						</Stack>
					</Scrollbars>

					{/* Logo Positioned at the Bottom */}
					{/* <Box
						position="absolute"
						bottom="50px" // Adjust this value to your desired spacing from the bottom
						left="50%"
						transform="translateX(-50%)" // Center the logo horizontally
					>
						<Image
							src={logoImg}
							width="800px" // Set specific width
							height="200px" // Set specific height
							objectFit="contain"
						/>
					</Box> */}
				</Box>
			</Box>
		</Box>
	);
}

// FUNCTIONS

export function SidebarResponsive(props) {
	// to check for active links and opened collapses
	let location = useLocation();
	const { logo, routes, colorMode, hamburgerColor, ...rest } = props;

	// this is for the rest of the collapses
	const [state, setState] = React.useState({});
	const mainPanel = React.useRef();
	// verifies if routeName is the one active (in browser input)
	const activeRoute = (routeName) => {
		return location.pathname === routeName ? "active" : "";
	};
	// Chakra Color Mode
	let activeBg = useColorModeValue("white", "navy.700");
	let inactiveBg = useColorModeValue("white", "navy.700");
	let activeColor = useColorModeValue("gray.700", "white");
	let inactiveColor = useColorModeValue("gray.400", "white");
	let sidebarActiveShadow = useColorModeValue("0px 7px 11px rgba(0, 0, 0, 0.04)", "none");
	let sidebarBackgroundColor = useColorModeValue("white", "navy.800");

	// this function creates the links and collapses that appear in the sidebar (left menu)
	const createLinks = (routes) => {
		return routes.map((prop, key) => {
			if (prop.redirect) {
				return null;
			}
			if (prop.category) {
				var st = {};
				st[prop["state"]] = !state[prop.state];
				return (
					<>
						<Text
							color={activeColor}
							fontWeight="bold"
							mb={{
								xl: "6px",
							}}
							mx="auto"
							ps={{
								sm: "10px",
								xl: "16px",
							}}
							py="12px">
							{document.documentElement.dir === "rtl" ? prop.rtlName : prop.name}
						</Text>
						{createLinks(prop.views)}
					</>
				);
			}
			return (
				<NavLink to={prop.layout + prop.path} key={key}>
					{activeRoute(prop.layout + prop.path) === "active" ? (
						<Button
							boxSize="initial"
							justifyContent="flex-start"
							alignItems="center"
							bg={activeBg}
							boxShadow={sidebarActiveShadow}
							mb={{
								xl: "6px",
							}}
							mx={{
								xl: "auto",
							}}
							ps={{
								sm: "10px",
								xl: "16px",
							}}
							py="12px"
							borderRadius="15px"
							_hover="none"
							w="100%"
							_active={{
								bg: "inherit",
								transform: "none",
								borderColor: "transparent",
							}}
							_focus={{
								boxShadow: "none",
							}}>
							<Flex>
								{typeof prop.icon === "string" ? (
									<Icon>{prop.icon}</Icon>
								) : (
									<IconBox
										bg="blue.500"
										color="white"
										h="30px"
										w="30px"
										me="12px">
										{prop.icon}
									</IconBox>
								)}
								<Text color={activeColor} my="auto" fontSize="sm">
									{document.documentElement.dir === "rtl"
										? prop.rtlName
										: prop.name}
								</Text>
							</Flex>
						</Button>
					) : (
						<Button
							boxSize="initial"
							justifyContent="flex-start"
							alignItems="center"
							bg="transparent"
							mb={{
								xl: "6px",
							}}
							mx={{
								xl: "auto",
							}}
							py="12px"
							ps={{
								sm: "10px",
								xl: "16px",
							}}
							borderRadius="15px"
							_hover="none"
							w="100%"
							_active={{
								bg: "inherit",
								transform: "none",
								borderColor: "transparent",
							}}
							_focus={{
								boxShadow: "none",
							}}>
							<Flex>
								{typeof prop.icon === "string" ? (
									<Icon>{prop.icon}</Icon>
								) : (
									<IconBox
										bg={inactiveBg}
										color="blue.500"
										h="30px"
										w="30px"
										me="12px">
										{prop.icon}
									</IconBox>
								)}
								<Text color={inactiveColor} my="auto" fontSize="sm">
									{document.documentElement.dir === "rtl"
										? prop.rtlName
										: prop.name}
								</Text>
							</Flex>
						</Button>
					)}
				</NavLink>
			);
		});
	};

	var links = <>{createLinks(routes)}</>;

	//  BRAND

	var brand = (
		<Box pt={"35px"} mb="8px">
			{logo}
			<HSeparator my="26px" />
		</Box>
	);

	// SIDEBAR
	const { isOpen, onOpen, onClose } = useDisclosure();
	const btnRef = React.useRef();
	// Color variables
	return (
		<Flex display={{ sm: "flex", xl: "none" }} ref={mainPanel} alignItems="center">
			<HamburgerIcon color={hamburgerColor} w="18px" h="18px" ref={btnRef} onClick={onOpen} />
			<Drawer
				isOpen={isOpen}
				onClose={onClose}
				placement={document.documentElement.dir === "rtl" ? "right" : "left"}
				finalFocusRef={btnRef}>
				<DrawerOverlay />
				<DrawerContent
					w="250px"
					maxW="250px"
					ms={{
						sm: "16px",
					}}
					my={{
						sm: "16px",
					}}
					borderRadius="16px"
					bg={sidebarBackgroundColor}>
					<DrawerCloseButton
						_focus={{ boxShadow: "none" }}
						_hover={{ boxShadow: "none" }}
					/>
					<DrawerBody maxW="250px" px="1rem">
						<Box maxW="100%" h="100vh">
							<Box>{brand}</Box>
							<Stack direction="column" mb="40px">
								<Box>{links}</Box>
							</Stack>
						</Box>
					</DrawerBody>
				</DrawerContent>
			</Drawer>
		</Flex>
	);
}

export default Sidebar;
