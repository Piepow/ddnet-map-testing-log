<?php

namespace DDNet\MapTestingLog\Support\Asset;

class Fetcher
{
    private $appUrl;

    public function __construct(string $appUrl)
    {
        $this->appUrl = $appUrl;
    }

    public function getLink(string $assetName)
    {
        return $this->appUrl . '/assets/' . $assetName;
    }
}
