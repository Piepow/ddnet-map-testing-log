<?php

namespace DDNet\MapTestingLog\Contracts\Support\View;

use Psr\Http\Message\ResponseInterface;

interface Renderer
{
    public function render(
        ResponseInterface $response,
        string $view,
        array $data
    ): ResponseInterface;

    public function fetch(string $view, array $data): string;
}
