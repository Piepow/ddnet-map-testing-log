<?php

namespace DDNet\MapTestingLog\Message\Component\Variants;

use DDNet\MapTestingLog\Message\Component;

class Attachment extends Component
{
    public $url;
    public $basename;
    public $extension;
    public $filesize;
    public $filesizeUnits;

    public function __construct(array $source)
    {
        $source = $source['attachment'];
        $this->url = $source['url'];
        $this->basename = $source['basename'];
        $this->extension = $source['extension'];
        $this->filesize = $source['filesize'];
        $this->filesizeUnits = $source['filesize-units'];
    }

    public static function isCorrectVariant($source): bool
    {
        return isset($source['attachment']);
    }
}
