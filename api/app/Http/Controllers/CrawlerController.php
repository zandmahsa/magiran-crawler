<?php

namespace App\Http\Controllers;

use App\Models\Author;
use App\Models\Paper;
use Illuminate\Http\Request;

class CrawlerController extends Controller
{
    public function index(Request $req)
    {
        if (!$req->hasFile('import')) {
            return response()->json([
                'message' => 'file not found'
            ], 404);
        }
        $file = $req->file('import');
        $file_ext = $file->getClientOriginalExtension();
        $file_name = $file->getClientOriginalName();
        $upload_path = $file->store('crawler', 'public');
        $json = file_get_contents($file);
        $to_array = json_decode($json, TRUE);
        // dd($to_array['res']);
        foreach ($to_array['res'] as $authors) {
            if (!Author::where('author', $authors['نام'])->first()) {
                Author::create([
                    'author' => $authors['نام']
                ]);
            }
        }
        foreach ($to_array['res'] as $authors) {
            $author = Author::where('author', $authors['نام'])->first();
            foreach ($authors['مقالات'] as $papers) {
                $duplicate_paper = Paper::where('link', $papers['لينک کوتاه'])->first();
                if (!$duplicate_paper) {
                    Paper::create([
                        'title' => $papers['عنوان'],
                        'o_authors' => $papers['نويسنده'],
                        'tags' => $papers['کليد واژه'],
                        'noe_maghale' => $papers['نوع مقاله'],
                        'lang' => $papers['زبان'],
                        'publisher' => $papers['انتشارات'],
                        'link' => $papers['لينک کوتاه'],
						'pages'=> $papers['صفحات'],
                        'author_id' => $author->id
                    ]);
                } else {
                    $duplicate_paper->update([
                        'title' => $papers['عنوان'],
                        'o_authors' => $papers['نويسنده'],
                        'tags' => $papers['کليد واژه'],
                        'noe_maghale' => $papers['نوع مقاله'],
                        'lang' => $papers['زبان'],
                        'publisher' => $papers['انتشارات'],
						'pages'=> $papers['صفحات'],
                    ]);
                }
            }
        }

        return response()->json([
            'message' => 'data imported successfully'
        ], 200);
    }
}
