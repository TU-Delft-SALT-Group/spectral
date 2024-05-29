import used from '$lib/utils';
import type {
	DockviewApi,
	DockviewGroupPanel,
	GroupPanelPartInitParameters,
	IContentRenderer,
	IDockviewGroupPanel,
	IGroupHeaderProps,
	IHeaderActionsRenderer,
	ITabRenderer,
	PanelUpdateEvent,
	Parameters
} from 'dockview-core';

import { type SvelteComponent, mount, unmount, type ComponentType } from 'svelte';

type Component<P extends Record<string, unknown>> = ComponentType<SvelteComponent<P>>;

abstract class AbstractSvelteRenderer<S extends Record<string, unknown>> {
	readonly _element: HTMLElement;
	readonly _component: Component<S>;
	protected _instance: Component<S> | undefined;

	get element() {
		return this._element;
	}

	get component() {
		return this._component;
	}

	constructor(component: Component<S>) {
		this._component = component;

		this._element = document.createElement('div');
		this.element.className = 'dv-vue-part';
		this.element.style.height = '100%';
	}

	dispose(): void {
		if (this._instance !== undefined) {
			unmount(this._instance);
		}
	}
}

export class SvelteRenderer<S extends Record<string, unknown>>
	extends AbstractSvelteRenderer<S>
	implements IContentRenderer, ITabRenderer
{
	private _props: S | undefined;

	constructor(component: Component<S>) {
		super(component);
	}

	init(parameters: GroupPanelPartInitParameters): void {
		this._props = parameters.params as S;

		this._instance = mount(this._component, {
			target: this._element,
			props: { ...this._props, api: parameters.api, title: parameters.title }
		}) as Component<S>;
	}

	update(event: PanelUpdateEvent<Parameters>): void {
		if (this._instance === undefined) {
			return;
		}

		const params = event.params.params as S;
		this._props = { ...(this._props as S), ...params };
	}
}

type TabRequirements<S = Record<string, unknown>> = {
	containerApi: DockviewApi;
	group: IDockviewGroupPanel;
	defaultProps: S;
};

export class SvelteTabActionRenderer<P extends Record<string, unknown>>
	extends AbstractSvelteRenderer<TabRequirements<P>>
	implements IHeaderActionsRenderer
{
	private _defaultProps: P;

	constructor(
		component: Component<TabRequirements<P>>,
		group: DockviewGroupPanel,
		defaultProps: P
	) {
		super(component);
		used(group);
		this._defaultProps = defaultProps;
	}

	init(params: IGroupHeaderProps): void {
		const props: TabRequirements<P> = {
			...params,
			defaultProps: this._defaultProps
		};

		this._instance = mount(this._component, {
			target: this._element,
			props
		}) as Component<TabRequirements<P>>;
	}
}
