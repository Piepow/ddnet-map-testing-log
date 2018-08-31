<?php

namespace DDNet\MapTestingLog\Support\View\Helpers;

use Parsedown;

class MarkdownParser extends Parsedown
{
    protected $safeMode = true;
}
