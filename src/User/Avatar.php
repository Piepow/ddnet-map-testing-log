<?php

namespace DDNet\MapTestingLog\User;

use DDNet\MapTestingLog\Support\Url;
use DDNet\MapTestingLog\Support\Container\Access as ContainerAccess;

class Avatar
{
    public $url;
    public $isAsset;

    private $size;

    public function __construct(string $url)
    {
        $this->size = 40;
        $this->url = $this->determineUrl($url);
    }

    private function determineUrl(string $url): string
    {
        if ($this->isDefaultAvatar($url)) {
            $this->isAsset = false;
            return $url;
        }

        $urlPath = parse_url($url)['path'];
        $urlPathComponents = explode('/', $urlPath);
        $lastDirectoryAndFile = array_slice($urlPathComponents, -2, 2);

        $lastDirectory = $lastDirectoryAndFile[0] . '/';
        $filename = $lastDirectoryAndFile[1];

        $avatarStoragePath = (
            ContainerAccess::$container
        )['config']['storage']['path'] . 'avatars/';

        $lastDirectoryPath = $avatarStoragePath . $lastDirectory;
        $filePath = $lastDirectoryPath . $filename;

        if (file_exists($filePath)) {
            $this->isAsset = true;
            return 'avatars/' . $lastDirectory . $filename;
        }

        if (Url::getHttpResponseCode($url) == 200) {
            if (!is_dir($lastDirectoryPath)) {
                mkdir($lastDirectoryPath, 0775, true);
            }

            if (!file_exists($filePath)) {
                copy($url . '?size=' . $this->size, $filePath);
            }

            $this->isAsset = true;
            return 'avatars/' . $lastDirectory . $filename;
        }

        $this->isAsset = false;
        return 'https://cdn.discordapp.com/embed/avatars/0.png?size=' . $this->size;
    }

    private function isDefaultAvatar(string $url): bool
    {
        $defaultAvatarUrlBase = 'https://cdn.discordapp.com/embed/avatars/';
        $defaultAvatarBasenames = [0, 1, 2, 3, 4];
        $defaultAvatarExtension = '.png';
        foreach ($defaultAvatarBasenames as $defaultAvatarBasename) {
            if ($url == $defaultAvatarUrlBase . $defaultAvatarBasename
                . $defaultAvatarExtension) {
                return true;
            }
        }
        return false;
    }
}
