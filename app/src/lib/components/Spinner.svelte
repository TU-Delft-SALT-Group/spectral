<div class="lds-ripple">
	<div></div>
	<div></div>
</div>

<style lang="postcss">
	.lds-ripple {
		display: inline-block;
		position: relative;
		aspect-ratio: 1;
		height: 100%;
	}
	.lds-ripple div {
		position: absolute;
		border: 2px solid theme(colors.foreground);
		opacity: 50%;
		border-radius: 50%;
		animation: lds-ripple 1s cubic-bezier(0, 0.2, 0.8, 1) infinite;
	}
	.lds-ripple div:nth-child(2) {
		animation-delay: -0.5s;
	}
	@keyframes lds-ripple {
		0% {
			top: 45%;
			left: 45%;
			width: 0;
			height: 0;
			opacity: 0;
		}
		4.9% {
			opacity: 0;
		}
		5% {
			opacity: 50%;
		}
		100% {
			top: 0;
			left: 0;
			width: 90%;
			height: 90%;
			opacity: 0;
		}
	}
</style>
