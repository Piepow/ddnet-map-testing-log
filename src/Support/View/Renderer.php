<?php

namespace DDNet\MapTestingLog\Support\View;

use DDNet\MapTestingLog\Contracts\Support\View\Renderer as RendererContract;
use Psr\Http\Message\ResponseInterface;
use RuntimeException;
use Throwable;

class Renderer implements RendererContract
{
    public $viewsPath;
    public $helpers;

    public function __construct(string $viewsPath = "", $helpers = [])
    {
        $this->viewsPath = $viewsPath;
        $this->helpers = $helpers;
    }

    public function render(
        ResponseInterface $response,
        string $view,
        array $data = []
    ): ResponseInterface {
        $output = $this->fetch($view, $data);
        $response->getBody()->write($output);
        return $response;
    }

    // Must return properly sanitized HTML
    public function fetch(string $view, array $data): string
    {
        $viewPath = $this->viewsPath . $view;
        if (!is_file($viewPath)) {
            throw new RuntimeException("View does not exist");
        }
        $helpers = $this->getHelpers($view);
        $data = array_merge($helpers, $data);

        try {
            ob_start();
            $this->includeWithProtectedScope($viewPath, $data);
            return ob_get_clean();
        } catch (Throwable $e) {
            ob_end_clean();
            throw $e;
        }
    }

    private function getHelpers($view)
    {
        $helpers = [];
        foreach ($this->helpers as $helperEntry) {
            if ($helperEntry['view'] == $view) {
                $helper = $helperEntry['helper'];
                $helpers[$helper['name']] = $helper['helper'];
            }
        }
        return $helpers;
    }

    private function includeWithProtectedScope(
        string $viewPath,
        array $data
    ) {
        extract($data);
        include $viewPath;
    }
}
