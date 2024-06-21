<script lang="ts">
	import { cn } from '$lib/utils';
	import { browser } from '$app/environment';

	export let recording = false;
	export let previewing: Blob | null = null;

	export let cameraInfo: MediaDeviceInfo | null;
	export let micInfo: MediaDeviceInfo | null;

	export let stopRecording: boolean;

	export let onStopRecording: (blob: Blob) => void = () => {};

	/**
	 * By default the video preview looks mirrored.
	 * If this is set to true, the mirroring will be
	 * corrected, which looks more natural in the preview.
	 */
	export let correctMirroring = true;

	export { className as class };
	let className = '';

	let mediaStream: MediaStream;
	let mediaRecorder: MediaRecorder;
	let recordingChunks: Blob[] = [];
	let videoElement: HTMLVideoElement;

	$: if (browser && videoElement) {
		if (previewing !== null) {
			try {
				videoElement.srcObject = previewing;
			} catch (err) {
				console.log(
					'Error setting previewing. Expected, more info: https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement/srcObject',
					{ err }
				);

				videoElement.srcObject = null;
				videoElement.src = URL.createObjectURL(previewing);
			}

			videoElement.muted = false; // Unmute the audio during playback
			videoElement.controls = true;
			videoElement.play();
		} else if (mediaStream) {
			videoElement.srcObject = mediaStream;
			videoElement.muted = true; // Mute the audio during recording
			videoElement.controls = false;
			videoElement.play();
		}
	}

	$: if (recording) {
		previewing = null;
	}

	$: if (stopRecording) {
		mediaStream
			.getTracks() // get all tracks from the MediaStream
			.forEach((track) => track.stop()); // stop each of them
	}

	export function toggleRecording() {
		if (recording) {
			recording = false;
			mediaRecorder.stop();
		} else {
			recording = true;
			mediaRecorder.start();
		}
	}

	export async function loadVideo(
		camneraInfo: MediaDeviceInfo | null,
		audioInfo: MediaDeviceInfo | null
	) {
		navigator.mediaDevices
			.getUserMedia({
				video: {
					deviceId: camneraInfo?.deviceId,
					width: { min: 1280 },
					height: { min: 720 }
				},
				audio: {
					deviceId: audioInfo?.deviceId
				}
			})
			.then((obtainedStream) => {
				mediaStream = obtainedStream;

				mediaRecorder = new MediaRecorder(mediaStream, { mimeType: 'video/webm' });

				mediaRecorder.ondataavailable = (event: BlobEvent) => {
					recordingChunks.push(event.data);
				};

				mediaRecorder.onstop = () => {
					const blob = new Blob(recordingChunks, { type: 'video/webm' });
					recordingChunks = [];
					onStopRecording(blob);
				};
			});
	}

	$: browser && loadVideo(cameraInfo, micInfo);
</script>

<video
	class={cn(
		`mx-auto aspect-video h-full w-full max-w-xl rounded bg-gray-300 shadow outline outline-destructive transition-all dark:bg-gray-600 ${recording ? 'outline-[4px]' : 'outline-0'} ${correctMirroring && previewing === null ? '-scale-x-100' : ''} `,
		className
	)}
	bind:this={videoElement}
>
	<track kind="captions" />
</video>
