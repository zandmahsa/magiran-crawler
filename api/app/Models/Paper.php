<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

use function PHPSTORM_META\map;

class Paper extends Model
{
    use HasFactory;

    protected $fillable = [
        'title',
        'o_authors',
        'tags',
        'noe_maghale',
        'lang',
        'publisher',
        'link',
        'author_id',
		'pages'
    ];

    public function authors()
    {
        return $this->belongsTo(Author::class);
    }
}
