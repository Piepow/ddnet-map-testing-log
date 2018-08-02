<?php

namespace DDNet\MapTestingLog\Message\Component;

use DDNet\MapTestingLog\Contracts\Support\View\Renderer as
    ViewRendererContract;
use DDNet\MapTestingLog\Message\Component;
use ReflectionClass;

class Renderer
{
    private $viewRenderer;
    private $subPath;
    private $stepSubPath;

    public function __construct(
        ViewRendererContract $viewRenderer,
        string $subPath,
        string $stepSubPath
    ) {
        $this->viewRenderer = $viewRenderer;
        $this->subPath = $subPath;
        $this->stepSubPath = $stepSubPath;
    }

    public function render(Component $component): string
    {
        $viewData = ['component' => $component];
        $viewBasename = $this->getViewBasename($component);
        if ($component::hasComponents()) {
            $viewData['messageComponentRenderer'] = new self(
                $this->viewRenderer,
                $this->subPath . $this->stepSubPath . $viewBasename . '/',
                $this->stepSubPath
            );
        }

        return $this->viewRenderer->fetch(
            $this->subPath . $this->stepSubPath . $viewBasename . '.phtml',
            $viewData
        );
    }

    private function getViewBasename(Component $component): string
    {
        $filename = (new ReflectionClass($component))->getShortName();
        return strtolower(preg_replace('/(?<!^)[A-Z]/', '-$0', $filename));
    }
}
