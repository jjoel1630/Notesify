import { HomeIcon } from "components/Icons/Icons";
import React, { useEffect, useRef, useState } from "react";
import dashRoutes from "routes";
import { useHistory } from "react-router-dom";
import { Box, Button, HStack, IconButton, Input, Progress, Text, VStack } from "@chakra-ui/react";
import { FaDownload, FaPause, FaPlay, FaUpload } from "react-icons/fa";
import Sidebar from "components/Sidebar/Sidebar";

export default function Dashboard(props) {
	const [audioUrl, setAudioUrl] = useState(null);
	const [audioError, setAudioError] = useState(null);
	const [isUploaded, setIsUploaded] = useState(true);
	const [file, setFile] = useState(null);
	const [fileError, setFileError] = useState(null);
	const [success, setSuccess] = useState(null);
	const [transcript, setTranscript] = useState(null);
	const [uploadDuration, setUploadDuration] = useState(null);

	const [isPlaying, setIsPlaying] = useState(false);
	const [audioElement, setAudioElement] = useState(null);
	const [durationState, setDurationState] = useState(0);
	const [currentTime, setCurrentTime] = useState(0);
	const [uploadedFile, setUploadedFile] = useState(null);

	const audioRef = useRef(null); // Reference to the audio element

	const history = useHistory();

	const handlePlayPause = () => {
		if (audioRef.current) {
			if (isPlaying) {
				audioRef.current.pause();
			} else {
				audioRef.current.play();
			}
			setIsPlaying(!isPlaying);
		}
	};

	const handleTimeUpdate = () => {
		setCurrentTime(audioElement.currentTime);
	};

	const retrieveAudio = async (fileId, duration) => {
		try {
			const getAudioRes = await fetch("http://127.0.0.1:5000/api/get_audio_id", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({
					file_id: fileId,
					duration: duration,
				}),
			});

			if (!getAudioRes.ok) {
				const errorData = await response.json();
				throw new Error(errorData.error || "Something went wrong");
			}

			const result = await getAudioRes.json();
			setTranscript(result.text.join(" "));
			const getAudioByteRes = await fetch(
				`http://127.0.0.1:5000/api/get_audio_byte?file_id=${result.document_id}`,
				{
					method: "GET",
				}
			);
			if (!getAudioByteRes.ok) {
				throw new Error("Network response was not ok");
			}
			const getAudioByteData = await getAudioByteRes.json();

			const getAudioBlob = await fetch(`data:audio/wav;base64,${getAudioByteData.audio}`); // Adjust MIME type as needed
			const getAudioBlobUrl = URL.createObjectURL(await getAudioBlob.blob());
			setAudioUrl(getAudioBlobUrl); // Set the audio URL for the <audio> element
			const realAudio = new Audio(getAudioBlobUrl);
			setAudioElement(realAudio);
			audioRef.current = realAudio;

			realAudio.addEventListener("loadedmetadata", () => {
				setDurationState(realAudio.duration);
			});

			realAudio.addEventListener("timeupdate", () => {
				setCurrentTime(realAudio.currentTime);
			});
			// console.log(getAudioBlobUrl);
		} catch (error) {
			console.log(error);
		}
	};

	const handleProgressClick = (event) => {
		const progressBar = event.target;
		const rect = progressBar.getBoundingClientRect();
		const clickPosition = event.clientX - rect.left;
		const progressBarWidth = rect.width;
		const clickPositionRatio = clickPosition / progressBarWidth;

		if (audioRef.current) {
			// Calculate the new time, ensuring it stays within the bounds of the audio duration
			const newTime = Math.min(
				Math.max(clickPositionRatio * durationState, 0),
				durationState
			);
			audioRef.current.currentTime = newTime;
			setCurrentTime(newTime);
		}
	};

	useEffect(() => {
		return () => {
			if (audioRef.current) {
				audioRef.current.pause();
				audioRef.current.remove();
			}
		};
	}, []);

	const handleFileChange = (event) => {
		const selectedFile = event.target.files[0];
		const allowedTypes = ["application/pdf", "text/plain", "application/x-latex", "image/jpeg"];

		// Check file type
		if (selectedFile && !allowedTypes.includes(selectedFile.type)) {
			setFileError("Please upload a valid file (PDF, TXT, LaTeX, JPG).");
			setFile(null);
		} else {
			setFile(selectedFile);
			setFileError(null);
		}
	};

	const handleUpload = async (event) => {
		const selectedFile = event.target.files[0];
		const allowedTypes = [
			"application/pdf",
			"text/plain",
			"application/x-latex",
			"text/x-tex", // Allow .tex files
			"application/x-tex", // Another option for .tex files
			"image/jpeg",
			"application/vnd.openxmlformats-officedocument.wordprocessingml.document", // .docx files
		];
		// Check file type
		if (selectedFile && !allowedTypes.includes(selectedFile.type)) {
			setFileError("Please upload a valid file (PDF, TXT, LaTeX, JPG).");
			setFile(null);
		} else {
			setFile(selectedFile);
			setFileError(null);
		}

		if (!selectedFile) {
			console.log("select file");
			setFileError("Please select a file to upload.");
			return;
		}

		setUploadedFile(selectedFile);

		// Convert file to base64
		const reader = new FileReader();
		reader.onloadend = async () => {
			const base64data = reader.result.split(",")[1]; // Get base64 string without the prefix

			try {
				const response = await fetch("http://127.0.0.1:5000/api/upload_file", {
					method: "POST",
					headers: {
						"Content-Type": "application/json",
					},
					body: JSON.stringify({
						name: selectedFile.name,
						type: selectedFile.type.split("/")[1],
						file_bin: base64data, // Send the base64 string
					}),
				});

				if (!response.ok) {
					const errorData = await response.json();
					throw new Error(errorData.error || "Something went wrong");
				}

				const result = await response.json();
				setSuccess(`File uploaded successfully! ID: ${result.id}`);
				setFileError(null);
				// setFile(null); // Clear the file input

				await retrieveAudio(result.id, 2);

				// const fileData = {
				// 	path: result.id,
				// 	name: file.name,
				// 	component: "dashboard",
				// 	layout: "/",
				// 	fileId: result.id,
				// 	audioId: "",
				// };

				// Retrieve existing files from local storage
				// const existingFiles = JSON.parse(localStorage.getItem("uploadedFiles")) || [
				// 	dashRoutes[0],
				// ];

				// Add the new file data to the existing array
				// existingFiles.push(fileData);

				// Store the updated array back into local storage
				// localStorage.setItem("uploadedFiles", JSON.stringify(existingFiles));

				// history.push(`/${fileData.fileId}`);
			} catch (error) {
				setFileError(`Error uploading file: ${error.message}`);
				setSuccess(null);
			}
		};

		// Read the file as a data URL (base64)
		reader.readAsDataURL(selectedFile);
	};

	useEffect(() => {
		console.log(uploadDuration);
	}, [uploadDuration]);

	const handleDownload = () => {
		if (audioUrl) {
			const a = document.createElement("a");
			a.href = audioUrl; // URL of the MP3 file
			a.download = "audiofile.mp3"; // Specify the name for the downloaded file
			document.body.appendChild(a);
			a.click();
			document.body.removeChild(a);
		}
	};

	return (
		<>
			<Box
				ml="350px"
				h="100vh"
				display="flex"
				alignItems="center"
				justifyContent="center"
				bg="transparent"
				position="relative"
				top="-35px">
				<VStack spacing={4} align="center" p={8} bg="transparent" h="max" justify="center">
					<Text
						fontSize="7xl" // Adjust font size as per your need
						// fontWeight="bold"
						color="white" // Adjust text color as needed
						fontFamily='"Dancing Script", cursive' // Add your custom font family here later
						mt="0" // Set margin-top to 0 to reduce the gap
						mb={1} // Add margin to space it nicely from the rest of the components
					>
						Notesify
					</Text>
					{/* Consistent dark background */}
					{/* Transcript Display */}
					<Box
						w="1000px" // Width remains the same
						h="550px" // Height remains the same
						bg="gray.700" // Darker background for the transcript area
						borderRadius="30px"
						display="flex"
						alignItems={file ? "start" : "center"}
						justifyContent={file ? "flex-start" : "center"}
						// p={file ? 4 : 0}
						overflowY={file ? "auto" : "hidden"}
						boxShadow="0 8px 20px rgba(0, 0, 0, 0.7)"
						// pl="40px"
						// pt="30px"
						// border="1px solid"
						// borderColor="gray.600" // Darker border for a document-like feel
					>
						{file ? (
							<Text
								fontSize="md"
								lineHeight="1.7"
								textAlign="left"
								ml="40px"
								mt="30px"
								mr="40px"
								color="white" // White text for contrast
								fontFamily="'Courier New', Courier, monospace" // Set typewriter font
								whiteSpace="pre-wrap"
								fontWeight="bold">
								{transcript || "Loading audio..."}
							</Text>
						) : (
							<Text fontSize="lg" color="gray.400" textAlign="center">
								{/* Lighter gray for the empty message */}
								No Transcript Uploaded
							</Text>
						)}
					</Box>
					<Box h="20px" />
					{/* Upload and Download Buttons */}
					<HStack spacing={4} justify="center">
						<Button
							leftIcon={<FaUpload />}
							colorScheme="blue"
							variant="solid"
							as="label">
							Upload
							<input type="file" hidden onChange={handleUpload} />
						</Button>

						<Input
							placeholder="Duration"
							type="number"
							size="md"
							width="150px"
							variant="outline" // Use the outline variant for full border
							color="white" // Dark text color for better visibility
							_placeholder={{ color: "gray.500" }} // Slightly lighter placeholder
							onChange={(e) => setUploadDuration(e.target.value)}
							borderColor="blue.300" // Border color to match the theme
							_focus={{
								borderColor: "blue.500", // Darker blue on focus
								boxShadow: "0 0 0 1px blue.500", // Subtle shadow on focus
							}}
							_hover={{
								borderColor: "blue.400", // Slightly darker blue on hover
							}}
						/>

						<Button
							leftIcon={<FaDownload />}
							colorScheme="blue"
							variant="outline"
							onClick={handleDownload}
							isDisabled={!file}>
							Download
						</Button>
					</HStack>
					<Box h="5px" />
					{/* Custom Audio Player */}
					{audioUrl && (
						<VStack w="800px" spacing={4} align="center">
							{/* Audio Progress Bar with Current Time and Duration aligned on left and right sides */}
							<HStack w="100%" spacing={4} align="center">
								{/* Current Time (Left) */}
								<Text fontSize="sm" color="gray.300" whiteSpace="nowrap">
									{" "}
									{/* Lighter gray for better contrast */}
									{formatTime(currentTime)}
								</Text>

								{/* Progress Bar */}
								<Box flex="1" onClick={handleProgressClick} cursor="pointer">
									<Progress
										value={(currentTime / durationState) * 100}
										size="xs"
										colorScheme="blue"
										borderRadius="md"
										sx={{
											"& > div": {
												borderRadius: "md",
											},
										}}
										height="4px" // Progress bar height
									/>
								</Box>

								{/* Duration (Right) */}
								<Text fontSize="sm" color="gray.300" whiteSpace="nowrap">
									{" "}
									{/* Lighter gray for better contrast */}
									{formatTime(durationState)}
								</Text>
							</HStack>

							{/* Play/Pause Button */}
							<IconButton
								icon={isPlaying ? <FaPause /> : <FaPlay />}
								colorScheme="blue"
								onClick={handlePlayPause}
								size="lg"
								aria-label={isPlaying ? "Pause" : "Play"}
								variant="ghost"
								fontSize="32px"
								_hover={{ bg: "transparent" }}
								_focus={{ boxShadow: "none", outline: "none", border: "none" }}
								_active={{ bg: "transparent", border: "none" }}
							/>
						</VStack>
					)}
				</VStack>
			</Box>
		</>
	);
}

// Format time in mm:ss
const formatTime = (time) => {
	const minutes = Math.floor(time / 60);
	const seconds = Math.floor(time % 60);
	return `${minutes}:${seconds < 10 ? `0${seconds}` : seconds}`;
};
