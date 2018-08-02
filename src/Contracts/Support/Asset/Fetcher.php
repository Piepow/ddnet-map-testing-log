<?php

namespace DDNet\MapTestingLog\Contracts\Support\Asset;

interface Fetcher
{
    public function getLink(string $assetName): string;
}
