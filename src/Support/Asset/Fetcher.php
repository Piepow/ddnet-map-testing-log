<?php

namespace DDNet\MapTestingLog\Support\Asset;

use DDNet\MapTestingLog\Contracts\Support\Asset\Fetcher as AssetFetcherContract;

class Fetcher implements AssetFetcherContract
{
    private $appUrl;

    public function __construct(string $appUrl)
    {
        $this->appUrl = $appUrl;
    }

    public function getLink(string $assetName): string
    {
        return $this->appUrl . '/assets/' . $assetName;
    }
}
